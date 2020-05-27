# Installing the Photon Management Daemon on a Lightwave Client

After you have installed and configured a domain on Lightwave, and joined a client to the domain, you can install the Photon Management Daemon on that client so that you can remotely manage it.

## Prerequisites

- Have an installed Lightwave server with configured domain controller on it.
- Have an installed Lightwave client that is joined to the domain.
- Verify that you have 100 MB free for the daemon installation on the client.

## Procedure

1. Log in to a machine with installed Lightwave client over SSH as an administrator.
2. Install the Photon Management Daemon.
	
	`# tdnf install pmd -y`
2. Start the Photon Management Daemon.

	`# systemctl start pmd`
3. Verify that the daemon is in an `active` state.

	`# systemctl status pmd`
4. (Optional) In a new console, use `curl` to verify that the Photon Management Daemon returns information.

	Use the root credentials for the local client to authenticate against the daemon service.
	`# curl https://<lightwave-client-FQDN>:2081/v1/info -u root`

5. (Optional) Create an administrative user for the Photon Management Daemon for your domain and assign it the domain administrator role.
	1. In a browser, go to https://*lightwave-server-FQDN*.
	1. On the Cascade Identity Services page, enter your domain name and click **Take me to Lightwave Admin**.
	2. On the Welcome page, enter administrative credentials for your domain and click **Login**.
	2. Click **Users & Groups** and click **Add** to create a new user.
	3. On the Add New User page, enter user name, at least one name, password, and click **Save**.
	3. Click the **Groups** tab, select the Administrators group, and click  **Membership**  to add the new user to the group.
	4. On the View Members page, select the user that you created, click **Add Member**, click **Save**, and click **Cancel** to return to the previous page.
