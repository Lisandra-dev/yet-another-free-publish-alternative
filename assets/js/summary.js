details = document.querySelectorAll("details.second");
details.forEach((targetDetail) => {
    console.log("detail", details)
    console.log("target", targetDetail)
    targetDetail.addEventListener("click", () => {
        details.forEach((detail) => {
            if (detail !== targetDetail && targetDetail.className == "second") {
                detail.removeAttribute("open");
                console.log("second")
            }
        });
    });
});

detailsF = document.querySelectorAll("details.first");
detailsF.forEach((targetDetailF) => {
    targetDetailF.addEventListener("click", () => {
        detailsF.forEach((detailF) => {
            if (detailF !== targetDetailF && targetDetailF.className == "first") {
                detailF.removeAttribute("open");
                console.log("premier")
            }
        });
    });
});

var admo_noblock = function(target) {
    var html = target.innerHTML;
    let select = '';
    let query = '';
    const adm = ['note', 'seealso', 'abstract', 'summary', 'tldr', 'info',
        'todo', 'tip',
        'hint', 'important', 'success', 'check', 'done', 'question',
        'help', 'faq', 'warning',
        'caution', 'attention', 'failure', 'fail', 'missing', 'danger',
        'error', 'bug', 'example', 'exemple', "abstract",
        'quote', 'cite'
    ];
    const p_search = /<p>[?!]{3}ad-([A-Za-zÀ-ÖØ-öø-ÿ]+)/gi;
    const found_p = html.match(p_search);
    let select_html = ''
    if (found_p) {
        const p_len = found_p.length;
        for (var i = 0; i < p_len; i++) {
            select = found_p[i].replace("!!!ad-", '');
            select = select.replace("???ad-", '');
            select = select.replace('<p>', '')
            query = "<p class='admo-note'>";
            select_html = '.admo-note'
            const replaced = new RegExp(`<p>[!?]{3}ad-${select}`, 'gi')
            const replaceit = html.match(replaced)
            console.log(html)
            for (var j = 0; j < replaceit.length; j++) {
                html = html.replace(replaceit[j], query.replace('<br>', ''));
                console.log(html)
            }
        }
        target.innerHTML = html;

    }
}
admo_noblock(document.querySelector('.content'))