// CF Pages middleware: return 410 Gone for attack-residue URLs (random-letter+digits.html pattern)
// These pages were mass-created by an attack and already removed; explicit 410 tells Google
// to de-index them faster than a 404 would.
// Middleware runs BEFORE clean-URL 308 redirects, so the pattern matches the raw path.

// Attack pattern: /a12345678901234.html — one lowercase letter + 14 digits
const ATTACK_PATTERN = /^\/[a-z]\d{14}\.html$/;

export async function onRequest(context) {
  const url = new URL(context.request.url);
  if (ATTACK_PATTERN.test(url.pathname)) {
    return new Response('Gone', {
      status: 410,
      headers: {
        'Cache-Control': 'public, max-age=86400',
        'X-Robots-Tag': 'noindex, nofollow',
      },
    });
  }
  return context.next();
}
