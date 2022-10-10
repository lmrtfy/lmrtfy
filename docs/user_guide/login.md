To use LMRTFY we need you to sign up with us to authenticate with our API. This step is necessary to
prevent malicious activity. 

You can use one of our **social logins** or just sign up with email and password.

With your account you can to the following things:

* deploy scripts as a callable function
* submit jobs and call cloud functions
* access the [LMRTFY Management Board](https://app.lmrt.fyi)

# Sign Up

Before you can login the first time you need to sign up. Currently, you have three options to do that:

* email address + password
* GitHub account
* Google account

If you sign up with email/password you will be required to verify your email address. 

# Login

When you run an LMRTFY actions that require a token you will automatically be asked to login. Each 
token is valid for 24 hours before you need to login again. If you allow cookies our authentication 
provider Auth0 will recognize you.

!!! info
    Tokens are currently valid for 24 hours. After that you will be requested to login again. That also means
    that you cannot have scripts deployed more than 24 hours right now. This will change soon so that you
    can deploy scripts longer than that.

    Just run `lmrtfy deploy <script> --local`again after 24h and you are fine if you need longer running
    deployments right now.)

