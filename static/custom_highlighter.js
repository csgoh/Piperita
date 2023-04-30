ace.define("ace/mode/custom_highlight_rules", ["require", "exports", "module", "ace/lib/oop", "ace/mode/text_highlight_rules"], function (require, exports, module) {
    var oop = require("ace/lib/oop");
    var TextHighlightRules = require("ace/mode/text_highlight_rules").TextHighlightRules;

    var CustomHighlightRules = function () {
        this.$rules = {
            "start": [
                { token: "keyword", regex: /title|colourtheme|lane/ },
                { token: "string", regex: /:.*/ },
                { token: "entity.name.function", regex: /\(start\)|\(end\)/ },
                { token: "variable", regex: /\[.*?\]/ },
                { token: "keyword.operator", regex: /->/ },
                { token: "constant.language", regex: /as/ },
            ],
        };
    };

    oop.inherits(CustomHighlightRules, TextHighlightRules);
    exports.CustomHighlightRules = CustomHighlightRules;
});

ace.define("ace/mode/custom", ["require", "exports", "module", "ace/lib/oop", "ace/mode/text", "ace/mode/custom_highlight_rules"], function (require, exports, module) {
    var oop = require("ace/lib/oop");
    var TextMode = require("ace/mode/text").Mode;
    var CustomHighlightRules = require("ace/mode/custom_highlight_rules").CustomHighlightRules;

    var Mode = function () {
        this.HighlightRules = CustomHighlightRules;
    };

    oop.inherits(Mode, TextMode);

    (function () {
        this.$id = "ace/mode/custom";
    }).call(Mode.prototype);

    exports.Mode = Mode;
});

// Initialize the ACE Editor with the custom mode
var editor = ace.edit("editor");
editor.setTheme("ace/theme/monokai");
editor.session.setMode("ace/mode/custom");

document.querySelector("form").addEventListener("submit", (event) => {
    event.preventDefault();
    document.getElementById("text").value = editor.getValue();
    event.target.submit();
});
