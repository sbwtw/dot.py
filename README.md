# dot.py
Useful tools to manage your dotfiles and more !

## Startup
Step 1. fork this repo to your accounts.

Step 2. clone your new repo.
```bash
git clone git@github.com:<Your Account>/dot.py.git
```

Step 3. add your dotfiles
```bash
# track dotfiles
./dot.py push ~/.vimrc

# track system config files
./dot.py push /etc/dnsmasq.conf

# move dotfiles to current directory, and create a symbol link to original
./dot.py push --symbol ~/.zshrc

...
```

Step 4. commit & push your backuped files to github or other place.
```bash
git add .
git commit -a -m "update collected files"
git push
```

## Tips

### work with system files
If you want tracking system files, `./dot.py` should be running with `sudo`. and ensure the `$HOME` environment variable is keeped.

Run this command to check, if `$HOME` is NOT keep, the output will be the `root`'s home directory.
```bash
sudo echo $HOME
```

Edit `/etc/sudoers` to keep environment variable.
```bash
Defaults env_keep += "HOME"
```

## More Usage
> you can add `-t` to first argument to do a test before really execute.

### Collect tracking files
> If a file is deploy as symbol link, the file doesn't need to collect.
```bash
# use -t flag to test
sudo ./dot.py -t collect

# real execute
sudo ./dot.py collect
```

### Deploy tracking files
```bash
# use -t flag to test
sudo ./dot.py -t deploy

# real execute
sudo ./dot.py deploy
```

### Remove tracking file
```bash
./dot.py pop <tracked_file>
```

### Track file with another name
```bash
# track /etc/vimrc named to sys-vimrc
./dot.py push --name sys-vimrc /etc/vimrc

# track $HOME/vimrc named to my-vimrc
./dot.py push --name my-vimrc $HOME/vimrc
```

### Track file with symbol link
`dot.py` will move file to current directory, and create a symbol link in original position.

The file tracking with symbol link will be update automatical when edit.
```bash
./dot.py push --symbol $HOME/.vimrc
```


# License
This project is licensed under the [MIT](LICENSE) license.
