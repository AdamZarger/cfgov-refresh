from wagtail.wagtailcore import blocks

from v1.atomic_elements import atoms, organisms
from v1.blocks import AbstractFormBlock


class ConferenceRegistrationForm(AbstractFormBlock):
    heading = blocks.CharBlock(required=False, help_text=(
        'Note: Additional form field options will appear in '
        'Preview and Publish modes.'
    ))
    code = blocks.CharBlock(label='GovDelivery Code')
    sessions = blocks.ListBlock(
        blocks.CharBlock(label='Session'),
        label='Sessions attending'
    )
    capacity = atoms.IntegerBlock(help_text=(
        'Enter an integer that will be the conference attendance limit.'
    ))
    success_message = blocks.RichTextBlock(
        help_text=(
            'Enter a message that will be shown on successful registration.'
        )
    )
    at_capacity_message = organisms.FullWidthText(
        help_text=(
            'Enter a message that will be shown when the event is at capacity.'
        )
    )
    failure_message = blocks.CharBlock(
        help_text=(
            'Enter a message that will be shown if the GovDelivery '
            'subscription fails.'
        )
    )

    class Meta:
        handler = 'data_research.handlers.ConferenceRegistrationHandler'
        template = '_includes/conference-registration-form.html'


# @todo move to v1 atomic elements
class LineChart(blocks.StructBlock):
    title = blocks.CharBlock(required=False)
    element_id = blocks.CharBlock(required=False)
    chart_type = blocks.CharBlock(required=False)
    market = blocks.CharBlock(required=False)
    report_type = blocks.CharBlock(required=False)
    data_source = blocks.CharBlock(
        required=False,
        help_text='Github raw CSV url')
    note = blocks.CharBlock(required=False)

    class Meta:
        icon = 'image'
        template = '_includes/molecules/line-chart.html'

    # how this works https://github.com/cfpb/cfgov-refresh/blob/12a5568f0e73ce016f98ae8a2d859219eb3ce01c/cfgov/v1/models/base.py#L416
    class Media:
        js = ['chart.js']
