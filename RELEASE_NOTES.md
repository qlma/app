# Qlma

## Release notes v1.0.0
Initial MVP release

## Release notes v1.0.1
- Added required first_name and last_name fields to SignUp and Profile forms.
- One message with multiple recipients is now stored in the database as multiple records with same message content. This allows archiving and deleting messages for certain user.
- Added message archiving feature.
- Added message deletion feature.
- Added message reply link feature. (NOTE! Sender is not yet automatically populated on new message form.)
- Messages navi is now shown in all messaging pages.
- Unread messages count is shown on all messaging pages.
- New message content field has a wysiwyg editor now. 
- Storing messaging-navi state and highlighting selected item
- Registered user is now sent a confirmation email with a token. Link in the email points to confirmation URL. User is activated and logged in after confirmation. Requires env vars SMTP_EMAIL_USER & SMTP_EMAIL_PASS.
- Staff can deactivate users with is_active
- Staff can flag users is_staff to provide access to admin pages
- Staff can change user_type and give wider access
- New user is notified about account inactivity
- New users are stricted from private information before admin assigns them a group
- Username is limited to 20 characters


