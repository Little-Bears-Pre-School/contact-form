import os

import functions_framework
import httpx
from flask import redirect

TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Website Contact Form Submission</title>
    <style media="all" type="text/css">
@media only screen and (max-width: 640px) {{
  .main p,
  .main td,
  .main span {{
    font-size: 16px !important;
  }}

  .wrapper {{
    padding: 8px !important;
  }}

  .content {{
    padding: 0 !important;
  }}

  .container {{
    padding: 0 !important;
    padding-top: 8px !important;
    width: 100% !important;
  }}

  .main {{
    border-left-width: 0 !important;
    border-radius: 0 !important;
    border-right-width: 0 !important;
  }}
}}
@media all {{
  .ExternalClass {{
    width: 100%;
  }}

  .ExternalClass,
  .ExternalClass p,
  .ExternalClass span,
  .ExternalClass font,
  .ExternalClass td,
  .ExternalClass div {{
    line-height: 100%;
  }}

  .apple-link a {{
    color: inherit !important;
    font-family: inherit !important;
    font-size: inherit !important;
    font-weight: inherit !important;
    line-height: inherit !important;
    text-decoration: none !important;
  }}

  #MessageViewBody a {{
    color: inherit;
    text-decoration: none;
    font-size: inherit;
    font-family: inherit;
    font-weight: inherit;
    line-height: inherit;
  }}
}}
</style>
  </head>
  <body style="font-family: Helvetica, sans-serif; -webkit-font-smoothing: antialiased; font-size: 16px; line-height: 1.3; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; background-color: #f4f5f6; margin: 0; padding: 0;">
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="body" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #f4f5f6; width: 100%;" width="100%" bgcolor="#f4f5f6">
      <tr>
        <td style="font-family: Helvetica, sans-serif; font-size: 16px; vertical-align: top;" valign="top">&nbsp;</td>
        <td class="container" style="font-family: Helvetica, sans-serif; font-size: 16px; vertical-align: top; max-width: 600px; padding: 0; padding-top: 24px; width: 600px; margin: 0 auto;" width="600" valign="top">
          <div class="content" style="box-sizing: border-box; display: block; margin: 0 auto; max-width: 600px; padding: 0;">

            <!-- START CENTERED WHITE CONTAINER -->
            <span class="preheader" style="color: transparent; display: none; height: 0; max-height: 0; max-width: 0; opacity: 0; overflow: hidden; mso-hide: all; visibility: hidden; width: 0;">This is preheader text. Some clients will show this text as a preview.</span>
            <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="main" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; background: #ffffff; border: 1px solid #eaebed; border-radius: 16px; width: 100%;" width="100%">

              <!-- START MAIN CONTENT AREA -->
              <tr>
                <td class="wrapper" style="font-family: Helvetica, sans-serif; font-size: 16px; vertical-align: top; box-sizing: border-box; padding: 24px;" valign="top">
                  <p style="font-family: Helvetica, sans-serif; font-size: 16px;
                            font-weight: normal; margin: 0; margin-bottom:
                            16px;"><small><b>Message</b></small><br>{body}</p>
                  <p style="font-family: Helvetica, sans-serif; font-size: 16px;
                            font-weight: normal; margin: 0; margin-bottom:
                            16px;"><small><b>Name</b></small><br>{sender_name}</p>
                  <p style="font-family: Helvetica, sans-serif; font-size: 16px;
                            font-weight: normal; margin: 0; margin-bottom:
                            16px;"><small><b>Email</b></small><br>{sender_email}</p>
                  <p style="font-family: Helvetica, sans-serif; font-size: 16px;
                            font-weight: normal; margin: 0; margin-bottom:
                            16px;"><small><b>Phone</b></small><br>{phone}</p>
                </td>
              </tr>

              <!-- END MAIN CONTENT AREA -->
              </table>

            <!-- START FOOTER -->
            <div class="footer" style="clear: both; padding-top: 24px; text-align: center; width: 100%;">
              <table role="presentation" border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%;" width="100%">
                <tr>
                  <td class="content-block" style="font-family: Helvetica, sans-serif; vertical-align: top; color: #9a9ea6; font-size: 16px; text-align: center;" valign="top" align="center">
                    <span class="apple-link" style="color: #9a9ea6; font-size:
                        16px; text-align: center;">Little Bears Pre-School,
                        Stadhampton, Oxfordshire</span>
                  </td>
                </tr>
                <tr>
                  <td class="content-block powered-by" style="font-family: Helvetica, sans-serif; vertical-align: top; color: #9a9ea6; font-size: 16px; text-align: center;" valign="top" align="center">
                  </td>
                </tr>
              </table>
            </div>

            <!-- END FOOTER -->
            
<!-- END CENTERED WHITE CONTAINER --></div>
        </td>
        <td style="font-family: Helvetica, sans-serif; font-size: 16px; vertical-align: top;" valign="top">&nbsp;</td>
      </tr>
    </table>
  </body>
</html>
"""

@functions_framework.http
def contact_form(request):
    # only bots will fill in this honeypot field
    if request.form.get("middle_name"):
        return redirect("https://little-bears.com/contact-success", code=302)

    sender_email = request.form["email"]
    sender_name = f"{request.form['first_name']} {request.form['last_name']}"
    html = TEMPLATE.format(
        body=request.form["message"],
        sender_email=sender_email,
        sender_name=sender_name,
        phone=request.form["phone"],
    )

    httpx.post(
        f'https://api.mailgun.net/v3/{os.getenv("MAILGUN_DOMAIN_NAME")}/messages',
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={
            "from": "hello@little-bears.com",
            "h:Reply-To": f"{sender_name} <{sender_email}>",
            "to": "hello@little-bears.com",
            "subject": "Website Contact Form Submission",
            "html": html,
        },
    )

    return redirect("https://little-bears.com/contact-success", code=302)