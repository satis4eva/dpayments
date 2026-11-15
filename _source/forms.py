from common import *


def quote_form(source="contact", button="Request a quote", quote_label="What would you like a quote for?",
               quote_placeholder="e.g. two portable card machines for a restaurant, plus payment links for deposits"):
    chans = [("in-person", "In person"), ("online", "Online"), ("phone", "Over the phone"), ("not-yet", "Not yet")]
    chan_html = "".join(
        f'<label class="choice"><input type="checkbox" name="channels[]" value="{v}"><span>{l}</span></label>'
        for v, l in chans)
    return f'''<form class="form-card" action="/send.php" method="post">
  <div class="form-alert error" data-form-alert hidden role="alert"></div>
  <input type="hidden" name="source" value="{source}">
  <div class="hp" aria-hidden="true">
    <label for="website-{source}">Leave this field empty</label>
    <input type="text" id="website-{source}" name="website" tabindex="-1" autocomplete="off">
  </div>
  <div class="form-row two">
    <div>
      <label for="name-{source}">Your name <span class="req">*</span></label>
      <input type="text" id="name-{source}" name="name" required autocomplete="name" maxlength="120">
    </div>
    <div>
      <label for="email-{source}">Email <span class="req">*</span></label>
      <input type="email" id="email-{source}" name="email" required autocomplete="email" maxlength="160">
    </div>
  </div>
  <div class="form-row two">
    <div>
      <label for="business-{source}">Business name <span class="opt">(optional)</span></label>
      <input type="text" id="business-{source}" name="business" autocomplete="organization" maxlength="160">
    </div>
    <div>
      <label for="phone-{source}">Phone <span class="opt">(optional)</span></label>
      <input type="tel" id="phone-{source}" name="phone" autocomplete="tel" maxlength="40">
    </div>
  </div>
  <div class="form-row two">
    <div>
      <label for="industry-{source}">Type of business <span class="opt">(optional)</span></label>
      <select id="industry-{source}" name="industry">
        <option value="">Choose one</option>
        <option>Retail / shop</option>
        <option>Caf&eacute;, restaurant or bar</option>
        <option>Trades / field services</option>
        <option>Ecommerce</option>
        <option>Professional services</option>
        <option>Health, beauty or wellness</option>
        <option>Events or markets</option>
        <option>Gym, club or memberships</option>
        <option>Travel or transport</option>
        <option>Other</option>
      </select>
    </div>
    <div>
      <label for="turnover-{source}">Monthly turnover <span class="opt">(optional)</span></label>
      <select id="turnover-{source}" name="turnover">
        <option value="">Choose a range</option>
        <option>Just starting / not sure</option>
        <option>Under &pound;5,000</option>
        <option>&pound;5,000 &ndash; &pound;20,000</option>
        <option>&pound;20,000 &ndash; &pound;100,000</option>
        <option>Over &pound;100,000</option>
      </select>
    </div>
  </div>
  <fieldset class="form-row">
    <legend class="label">How do you take payments today?</legend>
    <div class="choice-grid">{chan_html}</div>
  </fieldset>
  <div class="form-row">
    <label for="message-{source}">{quote_label}</label>
    <textarea id="message-{source}" name="message" maxlength="4000" placeholder="{quote_placeholder}"></textarea>
  </div>
  <button class="btn btn-primary" type="submit">{button} {ARROW}</button>
  <p class="form-note">We&rsquo;ll come back to you by email. No phone tag, no pressure. Please don&rsquo;t include card numbers. See our <a href="/privacy/">privacy notice</a>.</p>
</form>'''
