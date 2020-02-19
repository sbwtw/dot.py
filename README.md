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

## 
