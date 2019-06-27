# show ports in use
alias ports='sudo lsof -i -P -n | grep LISTEN '

alias webpack='npx webpack '
alias j='jobs '
alias dco='docker-compose '
alias p='python3 '
alias ll='ls -la '

# pretty-print json
alias json='python3 -m json.tool '

function mcd() {
    mkdir -p $1; cd $1;
}

