# DNS for derogue.art (GoDaddy)

Apply these records only after this repository’s GitHub Pages site exists and its custom domain is `derogue.art` (the `CNAME` file in this repo). Pointing DNS at GitHub before that file is in place risks a domain takeover.

## Expected live URLs

Once these records propagate and GitHub Pages finishes issuing the TLS certificate:

- https://derogue.art
- https://www.derogue.art

`www` redirects to the apex because the repository `CNAME` is `derogue.art`. Certificate issuance often takes from a few minutes up to 24 hours after DNS is correct. Enforce HTTPS in the repo’s Pages settings once GitHub offers the option.

The same pages also stay at https://roguebachata.com/derogue/ from the Rogue Bachata repo (`test-rogue-plan`). That repo’s root `CNAME` must remain `roguebachata.com`. Do not copy this file’s `CNAME` into that repository.

Until the certificate exists, GitHub may also publish https://goodfornothin.github.io/derogue.art/ and then redirect it to https://derogue.art.

## Remove GoDaddy parking first

The domain currently parks on GoDaddy Website Builder / forwarding addresses:

- `3.33.130.190`
- `15.197.148.33`

In GoDaddy → My Products → derogue.art → DNS → DNS Records, delete those A records and any AAAA records on `@` that are not the GitHub addresses below. Also remove:

- Domain forwarding (apex or www)
- “Website Builder” / parked-page connection
- Any existing `www` CNAME that is not `goodfornothin.github.io`

Leaving the parking addresses in place alongside GitHub’s A records keeps the site on the parking page.

## Apex `derogue.art`

GoDaddy host `@` (or leave the host blank if the UI means the apex). Add all four A records:

| Type | Name | Value | TTL |
| --- | --- | --- | --- |
| A | `@` | `185.199.108.153` | 1 Hour |
| A | `@` | `185.199.109.153` | 1 Hour |
| A | `@` | `185.199.110.153` | 1 Hour |
| A | `@` | `185.199.111.153` | 1 Hour |

IPv6, recommended alongside the A records:

| Type | Name | Value | TTL |
| --- | --- | --- | --- |
| AAAA | `@` | `2606:50c0:8000::153` | 1 Hour |
| AAAA | `@` | `2606:50c0:8001::153` | 1 Hour |
| AAAA | `@` | `2606:50c0:8002::153` | 1 Hour |
| AAAA | `@` | `2606:50c0:8003::153` | 1 Hour |

## `www.derogue.art`

One CNAME. The target is the GitHub user site, with no repository name on the end:

| Type | Name | Value | TTL |
| --- | --- | --- | --- |
| CNAME | `www` | `goodfornothin.github.io` | 1 Hour |

Do not turn on GoDaddy forwarding from `www` to the apex. GitHub Pages does that redirect itself, which is what allows HTTPS on both names.

## Check

```bash
dig derogue.art +noall +answer -t A
dig derogue.art +noall +answer -t AAAA
dig www.derogue.art +nostats +nocomments +nocmd
```

`A` / `AAAA` answers should be only the GitHub addresses above. `www` should be a CNAME to `goodfornothin.github.io`.

After GitHub shows the certificate as provisioned, open https://derogue.art and https://www.derogue.art. Optionally verify the domain on the GitHub account (Settings → Pages) and add the TXT record GitHub displays there, so another repo cannot claim `derogue.art`.
