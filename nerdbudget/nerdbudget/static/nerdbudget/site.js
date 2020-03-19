var nbHelper = {
    sortable: function (e, tr) {
        var $originals = tr.children();
        var $helper = tr.clone();
        $helper.children().each(function (index) {
            // Set helper cell sizes to match the original sizes
            $(this).width($originals.eq(index).width());
        });
        return $helper;
    },
};

$(function () {
    $('[data-toggle="tooltip"]').tooltip();
    $('[nb-create-icon]').html('<i class="fa fa-plus fa-fw text-success"></i>');
    $('[nb-update-icon]').html('<i class="fa fa-edit fa-fw text-primary"></i>');
    $('[nb-delete-icon]').html('<i class="fa fa-times fa-fw text-danger"></i>');

    $('[nb-move-icon]').html('<i class="fa fa-bars fa-fw text-muted"></i>');
    $('[nb-list-icon]').html('<i class="fa fa-list fa-fw"></i>');
    $('[nb-dollar-icon]').html('<i class="fa fa-usd fa-fw text-success"></i>');
    $('[nb-import-icon]').html('<i class="fa fa-download fa-fw"></i>');
    $('[nb-analysis-icon]').html('<i class="fa fa-cogs fa-fw"></i>');
    $('[nb-previous-icon]').html('<i class="fa fa-caret-left fa-fw"></i>');
    $('[nb-next-icon]').html('<i class="fa fa-caret-right fa-fw"></i>');

    $('table.table-sortable tbody').sortable({
        items: "tr:not(.ui-state-disabled)",
        helper: nbHelper.sortable
    });

    $('form').submit(function () {
        $(this)
            .find('button[type=submit]')
            .append('<span class="fa fa-fw fa-cog fa-spin ml-2"></span>')
            .attr('disabled', 'disabled');
        return true;
    });
});
