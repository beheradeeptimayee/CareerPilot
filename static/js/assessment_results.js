document.addEventListener('DOMContentLoaded', function () {

    const progressBars = document.querySelectorAll(
        '.result-progress-fill'
    );

    progressBars.forEach(function (bar) {

        const score = bar.dataset.score;

        bar.style.width = score + '%';

    });

});