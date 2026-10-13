"""Package native CI builds with provenance, instructions and checksums."""
import argparse
import hashlib
import pathlib
import plistlib
import shutil
import subprocess
import tarfile
import zipfile

parser = argparse.ArgumentParser()
parser.add_argument('--platform', choices=['windows-x64', 'linux-x64', 'macos-x64', 'macos-arm64'], required=True)
parser.add_argument('--tag', required=True)
args = parser.parse_args()
root = pathlib.Path(__file__).resolve().parents[1]
name = f'kaspa-ng-{args.tag}-{args.platform}'
out = root / 'release-dist'
package = root / 'target' / 'release-packages' / name
package.mkdir(parents=True, exist_ok=True)
out.mkdir(exist_ok=True)
exe = 'kaspa-ng.exe' if args.platform == 'windows-x64' else 'kaspa-ng'
source = root / 'target' / 'release' / exe
if args.platform.startswith('macos-'):
    contents = package / 'Kaspa NG Test.app' / 'Contents'
    executable = contents / 'MacOS' / exe
    executable.parent.mkdir(parents=True, exist_ok=True)
    with (contents / 'Info.plist').open('wb') as handle:
        plistlib.dump({'CFBundleExecutable': exe, 'CFBundleIdentifier': 'org.shantee-chris.kaspa-ng.test',
                      'CFBundleName': 'Kaspa NG Test', 'CFBundlePackageType': 'APPL',
                      'CFBundleShortVersionString': '2.0.1', 'CFBundleVersion': '2.0.1',
                      'LSMinimumSystemVersion': '15.0', 'NSHighResolutionCapable': True}, handle)
else:
    executable = package / exe
shutil.copy2(source, executable)
executable.chmod(0o755)
if args.platform.startswith('macos-'):
    # Ad-hoc integrity signature, not Developer ID or notarization.
    subprocess.run(['codesign', '--force', '--sign', '-', str(package / 'Kaspa NG Test.app')], check=True)
    subprocess.run(['codesign', '--verify', '--strict', str(package / 'Kaspa NG Test.app')], check=True)
shutil.copy2(root / 'LICENSE', package / 'LICENSE-Kaspa-NG.txt')
shutil.copy2(root / 'docs' / 'LICENSE-Rusty-Kaspa.txt', package / 'LICENSE-Rusty-Kaspa.txt')
shutil.copy2(root / 'docs' / 'TEST-RELEASE.md', package / 'LIESMICH.md')
commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
rust = subprocess.check_output(['rustc', '--version'], text=True).strip()
(package / 'BUILD-INFO.txt').write_text(f'NG commit: {commit}\nPlatform: {args.platform}\nToolchain: {rust}\nProfile: release\nRK commit: 6aa2c21ae8f2d4b7752e070213394c0ec90f7a20\n', encoding='utf-8')
if args.platform == 'windows-x64':
    archive = out / f'{name}.zip'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as handle:
        for path in sorted(package.rglob('*')):
            if path.is_file():
                handle.write(path, path.relative_to(package))
else:
    archive = out / f'{name}.tar.gz'
    with tarfile.open(archive, 'w:gz') as handle:
        handle.add(package, arcname=name)
with archive.open('rb') as handle:
    digest = hashlib.file_digest(handle, 'sha256').hexdigest()
(out / f'{archive.name}.sha256').write_bytes(f'{digest}  {archive.name}\n'.encode('ascii'))
print(f'Created {archive.name}: {digest}')
