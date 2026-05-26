# gameapi

Notes for pipx-installed tools

- Pipx installs user apps to `C:\Users\chakk\.local\bin` on Windows.
- To make these available in new PowerShell sessions (persistent for your user), run:

```powershell
[Environment]::SetEnvironmentVariable("PATH", $env:PATH + ";C:\Users\chakk\.local\bin", "User")
```

- After running the command, open a new terminal (or log out/in). Then verify:

```powershell
pipx --version
uv --version
```

If you prefer not to change PATH persistently, you can add it for the current session:

```powershell
$env:PATH += ";C:\Users\chakk\.local\bin"
uv --version
```
