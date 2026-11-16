(label) => {
  let best = null;
  for (const e of document.querySelectorAll('body *')) {
    const t = (e.innerText || '').replace(/\s+/g, ' ').trim();
    if (t !== label) continue;
    const r = e.getBoundingClientRect();
    if (r.width === 0 || r.height === 0 || r.y > 200) continue;
    if (!best || r.width * r.height < best[2]) best = [r.x + r.width / 2, r.y + r.height / 2, r.width * r.height];
  }
  return best;
}
