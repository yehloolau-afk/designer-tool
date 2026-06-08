// Netlify Function — proxy image generation to 火山方舟
exports.handler = async (event) => {
  const cors = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
  };
  if (event.httpMethod === 'OPTIONS') return { statusCode: 200, headers: cors, body: '' };

  const auth = event.headers['authorization'] || '';
  try {
    const resp = await fetch('https://ark.cn-beijing.volces.com/api/v3/images/generations', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': auth },
      body: event.body,
    });
    return {
      statusCode: resp.status,
      headers: { 'Content-Type': 'application/json', ...cors },
      body: await resp.text(),
    };
  } catch (e) {
    return {
      statusCode: 500,
      headers: { 'Content-Type': 'application/json', ...cors },
      body: JSON.stringify({ error: { message: e.message } }),
    };
  }
};
