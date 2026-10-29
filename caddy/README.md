# Production web server

Caddy replaces nginx, serving `/static/` and `/media/` from the existing volumes
and proxying application requests to `recipify:8000`.

This deployment intentionally keeps the existing FRP HTTP origin route. Public
HTTPS is handled upstream by Cloudflare; Caddy does not request a local certificate
for this HTTP-only site. No Certbot or renewal scripts are required. To terminate
HTTPS here later, configure an HTTPS FRP route and Caddy certificate automation.

There are no host ports published. Requests must come from a private address on a
Docker network. The legacy `daffodil-6-nginx-1` alias preserves the FRP destination.
Run `docker compose config --quiet` then `docker compose up -d --remove-orphans`.
Preserve the media/static and Caddy volumes across deployments; do not use `down -v`.
The old nginx config is retained for rollback.
