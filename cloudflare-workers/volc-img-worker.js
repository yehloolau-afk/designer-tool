// Cloudflare Worker — proxy image generation to 火山方舟
// Wall-clock timeout: 30s (vs Netlify free: 10s) — handles Seedream's 15-30s generation time
export default {
  async fetch(request) {
    const cors = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 200, headers: cors });
    }

    const auth = request.headers.get('Authorization') || '';

    try {
      const resp = await fetch('https://ark.cn-beijing.volces.com/api/v3/images/generations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': auth },
        body: request.body,
      });

      return new Response(await resp.text(), {
        status: resp.status,
        headers: { 'Content-Type': 'application/json', ...cors },
      });
    } catch (e) {
      return new Response(JSON.stringify({ error: { message: e.message } }), {
        status: 500,
        headers: { 'Content-Type': 'application/json', ...cors },
      });
    }
  },
};
