# logbook

logbook is simple CLI software that lets you log and tag events - as if you were 
a computer!

## Installing logbook to your computer

### 1. Download it

Get a binary from the [Releases](https://github.com/hs7t/logbook/releases/) tab. 
Binaries are available for three platforms:

- for Windows: `logbook-windows-[x86_64 or arm64].exe`
- for macOS: `logbook-macos-[arm64 or x86_64]`
- for Linux (x86-64 / arm64): `logbook-linux-[x86_64 or arm64]`

> [!TIP]
> Don't know what x86_64 or arm64 mean? If you're running Windows or Linux, your
  device is most likely to work with the x86_64 binary. If you're on an Apple Silicon 
  (M1, M2, M3...) Mac, choose the arm64 binary.

> [!WARN]
> **If you're using Linux or Mac:** If you want to use `logbook` on Linux or your Mac, you 
  have to mark the binary you downloaded as an executable. From your terminal, run this 
  command:
  ```bash
  chmod +x logbook-linux     # or logbook-macos
  ```

### 2. Add logbook to your PATH

This step is optional, but it's recommended as it allows you to use logbook from anywhere,

1. Move the logbook binary into a stable folder.
2. Run a command appropriate for your OS:
    - macOS (zsh):
        ```bash
        export PATH="$PATH:/path/to/stable/folder"
        source ~/.zshrc
        ```
    - Linux (bash):
        ```bash
        export PATH="$PATH:/path/to/stable/folder"
        source ~/.bashrc    # or ~/.profile, depending on your shell
        ```
    - Windows (PowerShell)
        ```powershell
        [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\path\to\stable\folder", "User")
        ```
> [!TIP]
> You should rename the binary to `logbook` (or `logbook.exe` on Windows)
  if you want to use it by just typing `logbook`.

## Using logbook

> [!TIP]
> You can add `--help` to the end of any command to get more info about it.

### Writing to your logbook

Logbook lets you write logs, like this:

```bash
logbook write "It's a sunny day!"
```

Isn't that cool? You can also assign *tags* to them:

```bash
logbook write "Ate hotdog" --tag life
logbook write "Forgot my keys" --tag lostitems
```

Tags can have *states*: a tag's state is like a numeric value that you can
increment and decrement using logs, like this:

```bash
logbook write "Forgot my keys" -t lostitems +1
```

...or like this:

```bash
logbook write "Stressed out because of exams" -t willtolive -10
```

In other words, they're a bit like a counter!

### Reading from your logbook

#### `read logs`

After writing some stuff to your logbook, you probably want to read it. To 
get a table with the logs you've written, do:

```bash
logbook read logs
```

By default, `read logs` will only show your 10 most recent logs. You can change
this:

```bash
logbook read logs 15    # will show 15 logs
```

There's some arguments you can use to customize the `read logs` output:

```bash
logbook read logs -t willtolive -t lostitems    # shows all logs that have 'willtolive' or 'lostitems' for tags
logbook read logs --sort tag    # sort items by their tag
logbook read logs --ascending   # output in ascending order
```

#### `read tags`

To get a nice overview of all tags (and their states), do:

```bash
logbook read tags
```
### Setting things up with `config`

#### `tag create`

`logbook` will try to be helpful and add tags for you automatically. If you
ever want to add tags yourself, you can do something like this:

```bash
logbook config tag create lostitems   # creates a new tag called lostitems
```

By default, that'll create a static (i.e. stateless) tag. You can make your new
tag a stateful one like so:

```bash
logbook config tag create lostitems --tag-kind stateful
```

#### `tag delete`

If you don't want a tag anymore, you can delete it:

```bash
logbook config tag delete carsseen  # deletes the tag 'carsseen'
```

Of course, your old logs assigned to this tag will need to be updated! You can 
choose what happens to them via the prompts `logbook` will give you.