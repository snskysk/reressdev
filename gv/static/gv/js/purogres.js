var bar = new ProgressBar.Line(container, {
strokeWidth: 4,
easing: 'easeInOut',
duration: 1400,
color: '#ea82ff',
trailColor: '#eee',
trailWidth: 1,
svgStyle: {width: '100%', height: '100%'}
});
bar.animate(1.0);
