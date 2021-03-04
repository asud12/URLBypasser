# URL Bypasser

A simple tool to bypass URL path restrictions. Can easily be extended to include extra checks by modifying the files within the `/resources` folder.

## Usage

```
$ python3 url_bypasser.py 
              __           __       __        __   __   ___  __
        |  | |__) |       |__) \ / |__)  /\  /__` /__` |__  |__)
        \__/ |  \ |___    |__)  |  |    /~~\ .__/ .__/ |___ |  \

        v1.0

        @_g0dmode
        @dcocking7

Usage: url_bypasser.py [url] [base_path] (optional)

        url                              - The url (e.g. https://google.com)
        base_path                        - The base path you want to access (e.g. /api)

Optional arguments:

        Attack Options:

                --verbs                  - Cycle through all the verbs for the specified path.
                --headers                - Cycle through all of the headers (defined in resources/payload_headers.py)
                --payloads (default)     - Try all of the payloads (defined in resources/payload_checks.txt)

        Request Options:

                --user-agent  [string]   - Cycle through all the verbs for the specified path.

        Filter Options:

                --hc  [code]             - The response code(s) to hide (e.g. --hc 302 or --hc 404,400)
                --hs  [size]             - The response size to hide (e.g. --hs 4096 or --hs 4096,1024
                --verbose                - Show debug information

Examples:

        url_bypasser.py https://www.google.com/ /api
        url_bypasser.py https://www.google.com/ /api --hc 302,404 --verbs
        url_bypasser.py https://www.google.com/ /api --hs 1024 --headers
```

## Credits

* Daniel Cocking - https://twitter.com/dcocking7 - For the original idea and testing.