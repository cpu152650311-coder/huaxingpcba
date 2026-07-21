// CF Pages Middleware — 410 Gone for all spam/attack URL patterns
// 998 spam URLs in GSC (93% of indexed pages) — patterns:
//   - /shop/pg/*  (4 URLs)
//   - /[a-z][0-9]{14,}.html  (115 URLs)  
//   - ?[a-z][0-9]{10,}.html  (879 URLs — www subdomain redirects here)

export async function onRequest(context) {
  const url = new URL(context.request.url);
  const path = url.pathname;
  const search = url.search;
  
  // Pattern: /shop/pg/* — Shopify injection spam
  if (path.startsWith('/shop/pg/')) {
    return new Response('Gone', { status: 410, headers: { 'Cache-Control': 'public, max-age=86400' } });
  }
  
  // Pattern: /[a-z][0-9]{14,}.html or /[a-z][0-9]{14,} — attack residuals
  if (/^\/[a-z]\d{14,}(\.html)?$/.test(path)) {
    return new Response('Gone', { status: 410, headers: { 'Cache-Control': 'public, max-age=86400' } });
  }
  
  // Pattern: query string spam — 879 URLs, highest volume
  // Examples: /?b29620232913809.html, /?x11211254112538.html
  if (/^[?&][a-z]\d{10,}\.html/.test(search)) {
    return new Response('Gone', { status: 410, headers: { 'Cache-Control': 'public, max-age=86400' } });
  }
  
  return context.next();
}
