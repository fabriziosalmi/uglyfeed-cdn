"""Wikimedia's User-Agent policy, applied in one place for every generator.

On 2026-09-10 all eleven feeds stopped generating at once, each with the same
line:

    ERROR - An unexpected error occurred during search:
            Expecting value: line 1 column 1 (char 0)

Nothing had changed here. Wikimedia began enforcing its User-Agent policy and
now answers a client without a descriptive one with HTTP 403 and a PLAIN TEXT
body, "Please set a user-agent and respect our robot policy". The JSON decoder
meets a 'P' where it expected a '{', and the error names the decoder rather than
the cause, which is why the failure reads like a parsing bug.

Measured against the live API on 2026-09-10:

    User-Agent absent or empty                      HTTP 403, text body
    'wikipedia (https://github.com/goldsmith/...)'  HTTP 403  <- the library default
    a UA naming the project and a contact           HTTP 200, JSON

The `wikipedia` package on PyPI is unmaintained (1.4.0, 2014) and ships that
second one, so every generator inherits a User-Agent Wikimedia now rejects.

This is called EXPLICITLY rather than run on import: an unused-import cleanup
would silently take the feeds down again, and the next person would spend the
morning on a JSONDecodeError that has nothing to do with JSON.

Policy: https://foundation.wikimedia.org/wiki/Policy:User-Agent_policy
"""
from __future__ import annotations

import wikipedia

# Wikimedia asks for the tool, a URL to reach whoever runs it, and a contact.
USER_AGENT = (
    'uglyfeed-cdn/1.0 '
    '(https://github.com/fabriziosalmi/uglyfeed-cdn; fabrizio.salmi@gmail.com)'
)


def configure() -> None:
    """Identify this client and stay inside the rate limit. Call before any query."""
    wikipedia.set_user_agent(USER_AGENT)
    # The same policy asks clients not to hammer the API. The library serialises
    # requests with a minimum interval when this is on; these feeds make a
    # handful of calls a day, so the cost is nil and the courtesy is not.
    wikipedia.set_rate_limiting(True)
