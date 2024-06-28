# Fixing Sendmail

If Sendmail is not behaving as expected or hangs during installation, it might be because FQDN is not set. 

Perform the following steps:  

1. Set an FQDN for your Photon OS machine. 

1. Run the following commands in the order below: 
        
    ```
    echo $(hostname -f) > /etc/mail/local-host-names
        
        cat > /etc/mail/aliases << "EOF"
            postmaster: root
            MAILER-DAEMON: root
            EOF
    
        /bin/newaliases
    
        cd /etc/mail
    
        m4 m4/cf.m4 sendmail.mc > sendmail.cf
    
        chmod 700 /var/spool/clientmqueue
    
        chown smmsp:smmsp /var/spool/clientmqueue
    ```

