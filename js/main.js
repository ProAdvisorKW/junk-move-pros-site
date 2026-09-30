(function(){
  // mobile nav
  var t = document.querySelector('.nav-toggle'), n = document.querySelector('.nav');
  if (t && n) t.addEventListener('click', function(){ n.classList.toggle('open'); });
  // faq accordion
  document.querySelectorAll('.faq-q').forEach(function(btn){
    btn.addEventListener('click', function(){
      btn.closest('.faq-item').classList.toggle('open');
    });
  });
  // quote form -> Supabase
  var form = document.getElementById('quote-form');
  if (form) form.addEventListener('submit', function(e){
    e.preventDefault();
    var cfg = window.JMP_CONFIG || {};
    var ok = document.getElementById('form-ok');
    var data = {
      name: form.name.value.trim(),
      email: form.email.value.trim(),
      phone: form.phone.value.trim(),
      service: form.service ? form.service.value : '',
      message: form.message.value.trim(),
      page: location.pathname
    };
    if (!cfg.SUPABASE_URL || !cfg.SUPABASE_ANON_KEY) {
      // No backend wired yet — fall back to a pre-filled text to the business line.
      var sms = 'sms:' + cfg.BUSINESS_PHONE_TEL + '?body=' + encodeURIComponent(
        'Hi Junk & Move Pros! I\'m ' + data.name + ' (' + data.phone + '). ' + data.service + ': ' + data.message);
      location.href = sms;
      return;
    }
    fetch(cfg.SUPABASE_URL + '/rest/v1/quote_requests', {
      method: 'POST',
      headers: {
        'apikey': cfg.SUPABASE_ANON_KEY,
        'Authorization': 'Bearer ' + cfg.SUPABASE_ANON_KEY,
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal'
      },
      body: JSON.stringify(data)
    }).then(function(r){
      if (r.ok) { ok.style.display = 'block'; form.reset(); form.scrollIntoView({behavior:'smooth'}); }
      else { alert('Something went wrong sending your request — please call or text us at ' + cfg.BUSINESS_PHONE); }
    }).catch(function(){
      alert('Something went wrong sending your request — please call or text us at ' + cfg.BUSINESS_PHONE);
    });
  });
})();
