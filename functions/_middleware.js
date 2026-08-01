/**
 * Huaxing PCBA — Security middleware for Cloudflare Pages
 * Blocks query-string attack residuals (spam injection pattern:
 * /?a12345678901234.html, /?shop/customer/entry, etc.)
 * These return 404 so Google drops them from the index.
 */
export async function onRequest(context) {
  const url = new URL(context.request.url);
  const q = url.search; // e.g. "?a12345678901234.html"

  // Attack patterns:
  // 1. ?<letter><10+ digits>.html  (mass spam injection)
  // 2. ?shop/...                    (magento-style attack path)
  if (q) {
    if (/^\?[a-z]\d{8,}/i.test(q) || /^\?shop\//i.test(q)) {
      return new Response('Not Found', { status: 404, statusText: 'Not Found' });
    }
  }
  return context.next();
}
