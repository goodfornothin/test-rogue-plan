# Publish this folder as derogue.art

This directory is the deRogue site at the repository root: `index.html`, `assets/`, `social/`, `.nojekyll`, and `CNAME` (`derogue.art`). DNS steps are in [DNS.md](DNS.md).

Creating `goodfornothin/derogue.art` (and `goodfornothin/derogue-art`) from the cloud agent failed. Both tokens on the VM returned HTTP 403:

- The `goodfornothin` fine-grained personal access token: `Resource not accessible by personal access token` on `POST /user/repos` and GraphQL `createRepository`.
- The Cursor GitHub App token: `Resource not accessible by integration`.

Neither token can create a repository. The site is ready to push once a repo exists.

## 1. Create the empty public repo

On GitHub, signed in as **goodfornothin**: https://github.com/new

- Repository name: `derogue.art` if GitHub accepts the dot, otherwise `derogue-art`
- Public
- Do not add a README, .gitignore, or license (this folder already has them)

Or, with a classic PAT or a fine-grained token that is allowed to create repositories:

```bash
gh repo create goodfornothin/derogue.art --public --description "deRogue static site for derogue.art"
```

## 2. Push this branch as `main`

This history is an orphan branch on the Rogue Bachata repo so it does not carry that site or its `CNAME`.

```bash
git clone --branch cursor/derogue-art-standalone-7291 --single-branch \
  https://github.com/goodfornothin/test-rogue-plan.git derogue-art
cd derogue-art
git remote set-url origin https://github.com/goodfornothin/derogue.art.git
git push -u origin cursor/derogue-art-standalone-7291:main
```

If the new repo was named `derogue-art`, change the remote URL to `https://github.com/goodfornothin/derogue-art.git`. The `CNAME` file stays `derogue.art` either way.

## 3. Enable GitHub Pages from `main` at `/`

```bash
gh api --method POST -H "Accept: application/vnd.github+json" \
  repos/goodfornothin/derogue.art/pages \
  --input - <<'EOF'
{"build_type":"legacy","source":{"branch":"main","path":"/"}}
EOF
```

Or in the browser: Settings → Pages → Deploy from a branch → `main` → `/ (root)` → Save.

The `CNAME` file sets the custom domain to `derogue.art` on the next Pages build. Then follow [DNS.md](DNS.md) at GoDaddy.

## Expected live URLs

After DNS propagates and GitHub Pages issues the certificate:

- https://derogue.art
- https://www.derogue.art

Do not change `CNAME` in `goodfornothin/test-rogue-plan`. That file must stay `roguebachata.com`. The subdirectory copy remains https://roguebachata.com/derogue/ after the companion pull request merges.
