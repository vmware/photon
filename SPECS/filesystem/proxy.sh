#
# proxy.sh:              Set proxy environment
#

sys=/etc/sysconfig/proxy
test -s $sys || exit 0
while read line ; do
    case "$line" in
    \#*|"") continue ;;
    esac
    eval val=${line#*=}
    case "$line" in
    PROXY_ENABLED=*)
        PROXY_ENABLED="${val}"
        ;;
    HTTP_PROXY=*)
        test "$PROXY_ENABLED" = "yes" || continue
        http_proxy="${val}"
        export http_proxy
        ;;
    HTTPS_PROXY=*)
        test "$PROXY_ENABLED" = "yes" || continue
        https_proxy="${val}"
        export https_proxy
        ;;
    FTP_PROXY=*)
        test "$PROXY_ENABLED" = "yes" || continue
        ftp_proxy="${val}"
        export ftp_proxy
        ;;
    GOPHER_PROXY=*)
        test "$PROXY_ENABLED" = "yes" || continue
        gopher_proxy="${val}"
        export gopher_proxy
        ;;
    SOCKS_PROXY=*)
        test "$PROXY_ENABLED" = "yes" || continue
        socks_proxy="${val}"
        export socks_proxy
        SOCKS_PROXY="${val}"
        export SOCKS_PROXY
        ;;
    SOCKS5_SERVER=*)
        test "$PROXY_ENABLED" = "yes" || continue
        SOCKS5_SERVER="${val}"
        export SOCKS5_SERVER
        ;;
    NO_PROXY=*)
        test "$PROXY_ENABLED" = "yes" || continue
        no_proxy="${val}"
        export no_proxy
        NO_PROXY="${val}"
        export NO_PROXY
    esac
done < $sys
unset sys line val

if test "$PROXY_ENABLED" != "yes" ; then
    unset http_proxy https_proxy ftp_proxy gopher_proxy no_proxy NO_PROXY socks_proxy SOCKS_PROXY SOCKS5_SERVER
fi
unset PROXY_ENABLED
#
# end of proxy.sh
