() => {
  // Every visible label and form value below the tab strip, in reading order.
  const out = [];
  for (const e of document.querySelectorAll('body *')) {
    const r = e.getBoundingClientRect(); const s = getComputedStyle(e);
    if (!(r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && r.y > 150)) continue;
    const pos = [Math.round(r.x), Math.round(r.y)];
    if (e.tagName === 'INPUT') {
      if (e.type === 'checkbox' || e.type === 'radio') out.push([pos, 'check', e.checked]);
      else if (e.type === 'password') out.push([pos, 'password', e.value ? '(set)' : '(empty)']);
      else if (!['file', 'button', 'hidden', 'submit'].includes(e.type)) out.push([pos, 'input', e.value]);
    } else if (e.tagName === 'TEXTAREA') out.push([pos, 'textarea', e.value]);
    else {
      let t = ''; for (const n of e.childNodes) if (n.nodeType === 3) t += n.textContent;
      t = t.trim(); if (t) out.push([pos, 'text', t]);
    }
  }
  out.sort((a, b) => (a[0][1] - b[0][1]) || (a[0][0] - b[0][0]));
  return out.map(x => x.slice(1).concat([x[0]]));
}
