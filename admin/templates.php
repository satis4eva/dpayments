<?php
/** Starter content for new pages, and the section blocks offered in the page editor. */

function tpl_hero(string $title, string $eyebrow = 'New page', string $crumb = ''): string {
    return '<section class="page-hero">
  <div class="container">
    <div class="crumbs"><a href="/">Home</a> / ' . e($crumb ?: $title) . '</div>
    <span class="eyebrow">' . e($eyebrow) . '</span>
    <h1>' . e($title) . '</h1>
    <p class="lede">Write a short introduction here. Click any text to change it.</p>
    <div class="btn-row"><a class="btn btn-primary" href="/contact/">Get a quote <span class="arrow" aria-hidden="true">&rarr;</span></a></div>
  </div>
</section>';
}

function block_html(string $type): string {
    $arrow = '<span class="arrow" aria-hidden="true">&rarr;</span>';
    $tick = '<span class="tick"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></span>';
    switch ($type) {
        case 'text':
            return '<section><div class="container narrow prose"><h2>Section heading</h2><p>Write your content here. You can make text <strong>bold</strong>, add links with Alt+click, and add more sections from the toolbar.</p><p>Add another paragraph by pressing Enter at the end of this one.</p></div></section>';
        case 'cards':
            $c = '';
            foreach (['shield' => 'First feature', 'clock' => 'Second feature', 'chart' => 'Third feature'] as $i => $t)
                $c .= '<div class="card">' . '<div class="icon">' . icon_svg($i) . '</div><h3>' . $t . '</h3><p>Describe this feature in a sentence or two.</p></div>';
            return '<section class="section-white"><div class="container"><div class="section-head"><span class="eyebrow">Features</span><h2>Section heading</h2><p class="lede">A short introduction to this section.</p></div><div class="grid g3">' . $c . '</div></div></section>';
        case 'image-text':
            return '<section><div class="container split v-center img-text"><div><span class="eyebrow">About</span><h2>Heading next to an image</h2><p class="lede">Explain something visually. Click the image to replace it with one of your own.</p><ul class="feature-list"><li>' . $tick . '<span>First point</span></li><li>' . $tick . '<span>Second point</span></li><li>' . $tick . '<span>Third point</span></li></ul></div><div><img src="/assets/img/placeholder.svg" alt="" class="cms-img"></div></div></section>';
        case 'text-image':
            return '<section class="section-white"><div class="container split v-center img-text"><div><img src="/assets/img/placeholder.svg" alt="" class="cms-img"></div><div><span class="eyebrow">Why us</span><h2>Image on the left, text on the right</h2><p class="lede">Click the image to replace it. Click any text to edit it.</p><a class="btn btn-primary" href="/contact/">Talk to us ' . $arrow . '</a></div></div></section>';
        case 'steps':
            $s = '';
            foreach (['Tell us what you need', 'We compare and recommend', 'We set it up', 'We stay on it'] as $t)
                $s .= '<div class="step"><div class="n"></div><div><h3>' . $t . '</h3><p>One or two sentences about this step.</p></div></div>';
            return '<section><div class="container split"><div class="sticky"><span class="eyebrow">How it works</span><h2>Simple steps</h2><p class="lede">A short introduction.</p></div><div class="steps">' . $s . '</div></div></section>';
        case 'image':
            return '<section class="section-tight"><div class="container"><img src="/assets/img/placeholder.svg" alt="" class="cms-img" style="width:100%"></div></section>';
        case 'faq':
            $q = '';
            foreach (['First question?', 'Second question?', 'Third question?'] as $t)
                $q .= '<details class="faq"><summary>' . $t . '</summary><div class="answer"><p>Write the answer here.</p></div></details>';
            return '<section class="section-white"><div class="container narrow"><div class="section-head"><span class="eyebrow">Questions</span><h2>Frequently asked questions</h2></div>' . $q . '</div></section>';
        case 'quote':
            return '<section class="section-dark"><div class="container narrow center"><p style="font-size:1.5rem;line-height:1.5;color:#fff;font-family:var(--font-head)">&ldquo;A short testimonial or key message goes here.&rdquo;</p><p>Name, Company</p></div></section>';
        case 'video':
            return '<section><div class="container narrow"><div style="position:relative;padding-top:56.25%;border-radius:var(--radius-lg);overflow:hidden;background:#000"><iframe src="https://www.youtube-nocookie.com/embed/VIDEO_ID" title="Video" style="position:absolute;inset:0;width:100%;height:100%;border:0" allowfullscreen loading="lazy"></iframe></div><p class="muted center">To change the video, switch to the HTML tab and replace VIDEO_ID with your YouTube video ID.</p></div></section>';
        case 'cta':
            return '<section class="section-tight"><div class="container"><div class="cta-band"><div><h2>Ready to get started?</h2><p>Tell us how you take payments and we&rsquo;ll do the rest.</p></div><div class="btn-row"><a class="btn btn-accent" href="/contact/">Get a quote ' . $arrow . '</a><a class="email-link" href="mailto:{{email}}">or email {{email}}</a></div></div></div></section>';
    }
    return '';
}

const BLOCKS = [
    'text' => 'Text', 'cards' => 'Feature cards', 'image-text' => 'Text + image', 'text-image' => 'Image + text',
    'steps' => 'Steps', 'image' => 'Wide image', 'faq' => 'FAQ', 'quote' => 'Quote / testimonial', 'video' => 'YouTube video', 'cta' => 'Call to action',
];

function page_template(string $tpl, string $title): string {
    $hero = tpl_hero($title);
    switch ($tpl) {
        case 'blank': return $hero;
        case 'landing': return $hero . block_html('cards') . block_html('image-text') . block_html('steps') . block_html('faq') . block_html('cta');
        default: return $hero . block_html('text') . block_html('cta');
    }
}
