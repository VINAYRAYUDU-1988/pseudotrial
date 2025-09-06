from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired, ValidationError
import datetime

class MyForm(FlaskForm):
    conditional_procedure = StringField("Conditional Procedure", validators=[DataRequired()])
    budget = DecimalField("Budget", validators=[DataRequired()])
    site_id = IntegerField("Site ID", validators=[DataRequired()])

    screening_visit = DecimalField("Screening Visit")
    baseline_visit = DecimalField("Baseline Visit")

    visit1 = DecimalField("Visit 1")
    visit2 = DecimalField("Visit 2")
    visit3 = DecimalField("Visit 3")
    visit4 = DecimalField("Visit 4")
    visit5 = DecimalField("Visit 5")
    visit6 = DecimalField("Visit 6")
    visit7 = DecimalField("Visit 7")
    visit8 = DecimalField("Visit 8")
    visit9 = DecimalField("Visit 9")
    visit10 = DecimalField("Visit 10")

    end_of_treatment = DecimalField("End of Treatment")
    follow_up = DecimalField("Follow up")
    end_of_study = DecimalField("End of Study")

    effective_date = DateField("Effective Date", format="%Y-%m-%d", validators=[DataRequired()])
    term_date = DateField("Term Date", format="%Y-%m-%d", validators=[DataRequired()])

    submit = SubmitField("Submit")

    # Custom validator for effective_date
    def validate_effective_date(self, field):
        min_date = datetime.date(2024, 1, 1)
        if field.data < min_date:
            raise ValidationError("Effective Date must be on or after 01-Jan-2024.")

    # Custom validator for term_date
    def validate_term_date(self, field):
        max_date = datetime.date(2030, 12, 31)
        if field.data > max_date:
            raise ValidationError("Term Date must be on or before 31-Dec-2030.")