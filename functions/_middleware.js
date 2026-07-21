// CF Pages Middleware — 410 Gone for spam/attack URLs  
// Matches BEFORE static file serving — instant removal signal to Google

export async function onRequest(context) {
  const url = new URL(context.request.url);
  const path = url.pathname;
  const search = url.search;
  
  // Pattern 1: /shop/pg/* — Shopify injection spam (highest priority)
  if (path.startsWith('/shop/pg/')) {
    return new Response('Gone', { status: 410, headers: { 'Cache-Control': 'public, max-age=86400' } });
  }
  
  // Pattern 2: /[a-z][0-9]{14,} or /[a-z][0-9]{14,}.html — attack residuals
  // Examples: /k36492704546154.html, /p38016353419410.html
  if (/^\/[a-z]\d{14,}(\.html)?$/.test(path)) {
    return new Response('Gone', { status: 410, headers: { 'Cache-Control': 'public, max-age=86400' } });
  }
  
  // Pattern 3: Query string spam — strip and redirect to clean URL
  // Examples: /?m46291354775938.html, /?x11211254112538.html
  if (/^[?&][a-z]\d{10,}/.test(search)) {
    return Response.redirect(url.origin + path, 301);
  }
  
  // Not spam — continue to static file
  return context.next();
}
