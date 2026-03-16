Here is your Quick Reference Guide for maintaining and reconfiguring the posims project.

1. Project Reference Summary

Project Root: /home/muazzam/pos-project/PosIms

Virtual Env: /home/muazzam/pos-project/PosIms/venv

Systemd Service: posims.service

Systemd Socket: posims.socket

Nginx Config: /etc/nginx/sites-available/posims

Gunicorn Socket Path: /run/posims.sock

2. Common Maintenance Commands
If you update your Python code:
code
Bash
download
content_copy
expand_less
cd ~/pos-project/PosIms
source venv/bin/activate
# Pull code, migrate, etc.
python manage.py migrate
python manage.py collectstatic --noinput
# RESTART GUNICORN TO APPLY CHANGES
sudo systemctl restart posims
If you change the .service or .socket files:
code
Bash
download
content_copy
expand_less
sudo systemctl daemon-reload
sudo systemctl restart posims.socket posims.service
If you change the Nginx config:
code
Bash
download
content_copy
expand_less
sudo nginx -t && sudo systemctl restart nginx
3. Troubleshooting (Where to look for errors)
Issue	Command to check
Site is down (502 Bad Gateway)	sudo journalctl -u posims -f
Nginx won't start	sudo nginx -t or sudo systemctl status nginx
Static files/Images not loading	Check Nginx logs: sudo tail -f /var/log/nginx/error.log
Gunicorn won't start	sudo systemctl status posims.service
4. How to add a new domain or change settings

Edit Nginx: sudo nano /etc/nginx/sites-available/posims

Update server_name.

Update alias paths if you move folders.

Edit Django settings.py: nano ~/pos-project/PosIms/posIms/settings.py

Update ALLOWED_HOSTS.

Update SSL:

code
Bash
download
content_copy
expand_less
sudo certbot --nginx -d newdomain.com
5. Managing Service States

Stop the app: sudo systemctl stop posims.socket posims.service

Start the app: sudo systemctl start posims.socket

Check if running: sudo systemctl status posims.socket

6. Security Reminder

If you ever create a new project under a different user, always remember the "Gatekeeper" rule:
Nginx (the www-data user) must have execute (755) permissions on the home directory of the user where the code lives:
chmod 755 /home/muazzam

You are now fully set up! Your POS system is running securely on Gunicorn and Nginx with SSL.