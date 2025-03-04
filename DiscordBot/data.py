from datetime import datetime

import cuid
import discord


class ReportData:
    SUMMARY = """## Message:
- Author: {offender}
- Content: {content}
- Attachments: {attachments}
- Link to Message: {link}
## Report Details:
- Reason: {reason}
- Abuse Type: {abuse_type}
- Abuse Description: {abuse_description}
- Unwanted Requests: {unwanted_requests}
- Multiple Requests: {multiple_requests}
- Approximate Requests: {approximate_requests}
- Complied with Requests: {complied_with_requests}
## Additional Information:
- Minor Participation: {minor_participation}
- Contained you or the person on behalf of whom this report is being filed: {contain_yourself}
- Encouraged self-harm: {encourage_self_harm}
- Additional information provided: {additional_info}
"""

    MODERATOR_NOTES = """## Moderator Notes:
- Report ID: {id}
- Priority: {priority}

- Created by: {reporter}
 - Created at: {date} (UTC)
 - Completed at: {completed_at} (UTC)
- On behalf of: {on_behalf_of}
- Reported User Blocked: {block_user}
"""

    def __init__(self):
        self.id = cuid.cuid()
        self.report_started_at = datetime.utcnow()
        self.report_completed_at = None
        self.reporter = None
        self.message = None
        self.attachments = None
        self.on_behalf_of = None
        self.reason = None
        self.abuse_type = None
        self.abuse_description = None
        self.unwanted_requests = None
        self.multiple_requests = None
        self.approximate_requests = None
        self.complied_with_requests = None
        self.minor_participation = None
        self.contain_yourself = None
        self.encourage_self_harm = None
        self.additional_info = None
        self.blocked_user = None

    @property
    def raw_priority(self) -> int:
        """
        Naive priority calculation based on certain fields.
        """
        risk = sum(
            [
                self.multiple_requests * 2 if self.multiple_requests else 0,
                self.complied_with_requests if self.complied_with_requests else 0,
                self.minor_participation * 3 if self.minor_participation else 0,
                self.encourage_self_harm * 3 if self.encourage_self_harm else 0,
            ]
        )

        return risk

    @property
    def priority(self) -> str:
        """
        Naive priority calculation based on certain fields.
        """
        if self.raw_priority <= 1:
            return "Low"

        if self.raw_priority == 2:
            return "Medium"

        return "High"

    @property
    def summary(self) -> str:
        """
        Generate a summary of the report.
        """
        return ReportData.SUMMARY.format(
            offender=self.message.author.name,
            content=self.message.content,
            attachments=self._human_readable(self.attachments),
            link=self._human_readable(self.message.jump_url),
            reason=self.reason,
            abuse_type=self.abuse_type,
            abuse_description=self.abuse_description,
            unwanted_requests=self._human_readable(self.unwanted_requests),
            multiple_requests=self._human_readable(self.multiple_requests),
            approximate_requests=self._human_readable(self.approximate_requests),
            complied_with_requests=self._human_readable(self.complied_with_requests),
            minor_participation=self._human_readable(self.minor_participation),
            contain_yourself=self._human_readable(self.contain_yourself),
            encourage_self_harm=self._human_readable(self.encourage_self_harm),
            additional_info=self._human_readable(self.additional_info),
        )

    @property
    def moderator_summary(self) -> str:
        """
        Generate a summary of the report for the moderator.
        """
        return (
            "New user report created. Please review the following report and take"
            " necessary action.\n"
            + ">>> "
            + ReportData.MODERATOR_NOTES.format(
                id=self.id,
                priority=self.priority,
                date=self.report_started_at,
                completed_at=self.report_completed_at,
                reporter=self.reporter.name,
                on_behalf_of=self.on_behalf_of if self.on_behalf_of else "themselves",
                block_user=self._human_readable(self.blocked_user),
            )
            + self.summary
        )

    @property
    def user_summary(self) -> str:
        """
        Generate a summary of the report for the user.
        """
        return ">>> " + self.summary

    def _human_readable(self, value: str) -> str:
        """
        Convert a boolean values and None to human readable strings.
        """
        if isinstance(value, bool):
            return "Yes" if value else "No"
        if value is None:
            return "N/A"
        return value


class AutoReportData:
    SUMMARY = """## Message:
- Author: {offender}
- Content: {content}
- Attachments: {attachments}
- Link to Message: {link}
## Report Details:
- Contains Sextortion: {sextortion}
- Contains Nudity: {nudity}
- Minor Participation: {minor_participation}
- Includes Self-harm: {encourage_self_harm}
"""

    MODERATOR_NOTES = """## Moderator Notes:
- Report ID: {id}
- Priority: {priority}
- Created at: {date} (UTC)
"""

    def __init__(
        self,
        message: discord.Message,
        *,
        is_sextortion: bool,
        encourage_self_harm: bool,
        minor_participation: bool,
        nudity: bool,
    ):
        self.id = cuid.cuid()
        self.report_started_at = datetime.utcnow()
        self.message = message  # when generating report -> get the message link
        self.attachments = (
            "\n" + "\n".join([" - " + str(a) + "." for a in message.attachments])
            if message.attachments
            else None
        )
        self.link = message.jump_url

        # if true -> automatically generate report
        self.is_sextortion = is_sextortion  # text classifier

        # if both of these true -> automatically generate report (CSAM)
        self.minor_participation = (
            minor_participation  # image classifer (cats vs. kittens)
        )
        self.nudity = nudity  # image classifer (cats vs. clothed cats)

        self.encourage_self_harm = encourage_self_harm  # text classifier

    @property
    def raw_priority(self) -> int:
        """
        Naive priority calculation based on certain fields.
        """
        risk = sum(
            [
                self.minor_participation * 3 if self.minor_participation else 0,
                self.encourage_self_harm * 3 if self.encourage_self_harm else 0,
            ]
        )

        return risk

    @property
    def priority(self) -> str:
        """
        Naive priority calculation based on certain fields.
        """
        if self.raw_priority <= 1:
            return "Low"

        if self.raw_priority == 2:
            return "Medium"

        return "High"

    @property
    def moderator_summary(self) -> str:
        """
        Generate a summary of the report for the moderator.
        """
        return (
            "New report automatically generated. Please review the following report and"
            " take necessary action.\n"
            + ">>> "
            + AutoReportData.MODERATOR_NOTES.format(
                id=self.id,
                priority=self.priority,
                date=self.report_started_at,
            )
            + AutoReportData.SUMMARY.format(
                offender=self.message.author.name,
                content=self.message.content,
                attachments=self._human_readable(self.attachments),
                link=self._human_readable(self.link),
                sextortion=self._human_readable(self.is_sextortion),
                nudity=self._human_readable(self.nudity),
                minor_participation=self._human_readable(self.minor_participation),
                encourage_self_harm=self._human_readable(self.encourage_self_harm),
            )
        )

    def _human_readable(self, value: str) -> str:
        """
        Convert a boolean values and None to human readable strings.
        """
        if isinstance(value, bool):
            return "Yes" if value else "No"
        if value is None:
            return "N/A"
        return value
