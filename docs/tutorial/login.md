To use LMRTFY you need to login to get an API token. The API token is necassary to 

* deploy scripts as a callable function
* submit jobs as call cloud functions

When you run an LMRTFY actions that require a token you will automatically be asked to login. Each 
token is valid for 24h before you need to relogin. If you allow cookies, you will probably not
have to login again because the authentication provider Auth0 recognizes you.

!!! info
    Tokens are currently valid for 24 hours. After that you will be requested to login again. That also means
    that you cannot have scripts deployed more than 24 hours right now. This will change soon so that you
    can deploy scripts longer than that.

    Just run `lmrtfy deploy <script> --local`again after 24h and you are fine if you need longer running
    deployments right now.)

## Sign-Up

Before you can login the first time you need to sign up. Currently, you have two options to do that:

* email adress + password
* google account

If you would like to sign up with another social login (e.g. GitHub) please let us know so that we
can prioritize this issue.