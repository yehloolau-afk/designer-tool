// Netlify Function — proxy video task submit + poll to 火山方舟
exports.handler = async (event) => {
  const cors = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  };
  if (event.httpMethod === 'OPTIONS') return { statusCode: 200, headers: cors, body: '' };

  const auth = event.headers['authorization'] || '';
  const BASE = 'https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks';

  let url = BASE;
  if (event.httpMethod === 'GET' && event.queryStringParameters?.taskId) {
    url = `${BASE}/${event.queryStringParameters.taskId}`;
  }

  try {
    const resp = await fetch(url, {
      method: event.httpMethod,
      headers: { 'Content-Type': 'application/json', 'Authorization': auth },
      body: event.httpMethod === 'POST' ? event.body : undefined,
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
