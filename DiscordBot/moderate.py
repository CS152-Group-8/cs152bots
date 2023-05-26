from enum import Enum, auto
from typing import List

import discord
from data import ReportData
from messages import GenericMessage, ModerateMessage, ReportStartMessage


class State(Enum):
    MODERATE_START = auto()
    AWAITING_MESSAGE = auto()
    MESSAGE_IDENTIFIED = auto()

    AWAITING_SEXTORTION_VIOLATION = auto()
    AWAITING_ADDITIONAL_DATA_COLLECTION_CONFIRM = auto()

    AWAITING_ADVERSARIAL_REPORTING = auto()
    MODERATE_COMPLETE = auto()


class Moderate:
    LIST_KEYWORD = "list"
    START_KEYWORD = "handle"
    CANCEL_KEYWORD = "cancel"
    HELP_KEYWORD = "help"
    YES_KEYWORDS = {"yes", "y"}
    NO_KEYWORDS = {"no", "n"}
    SKIP_KEYWORD = "skip"

    def __init__(self, client: discord.Client) -> None:
        self.state = State.MODERATE_START
        self.client = client
        self.handling_report: ReportData = None
        self.report_idx = None

    async def handle_message(self, message: discord.Message) -> List[str]:
        """
        This function makes up the meat of the moderator-side reporting flow. reports only on
        setortion violations.
        """
        if message.content == self.SKIP_KEYWORD:
            if self.state in self.SKIP_STAGES:
                prev_state = self.state
                self.state = self.SKIP_STAGES[prev_state][0]
                return self.SKIP_STAGES[prev_state][1]
            else:
                return GenericMessage.INVALID_SKIP

        if message.content == self.CANCEL_KEYWORD:
            self.state = State.MODERATE_COMPLETE
            return GenericMessage.CANCELED

        if self.state == State.MODERATE_START:
            self.state = State.AWAITING_MESSAGE
            return [ReportStartMessage.START, ReportStartMessage.MODERATE_REQUEST]

        if self.state == State.AWAITING_MESSAGE:
            report_id = message.content
            for report in self.client.open_reports:
                if report_id == report.id:
                    self.handling_report = report
                    self.state = State.MESSAGE_IDENTIFIED
                    return ReportStartMessage.REPORT_IDENTIFIED.format(
                        report_id=report_id, content=report.message.author.name
                    )
            return ReportStartMessage.INVALID_REPORTID

        if self.state == State.MESSAGE_IDENTIFIED:
            if message.content.lower() in self.YES_KEYWORDS:
                self.state = State.AWAITING_SEXTORTION_VIOLATION
                await message.channel.send(self.handling_report.moderator_summary)
                return ModerateMessage.IS_SEXTORTION_VIOLATION
            elif message.content.lower() in self.NO_KEYWORDS:
                self.state = State.AWAITING_MESSAGE
                return ReportStartMessage.REQUEST_MSG
            else:
                return GenericMessage.INVALID_YES_NO

        if self.state == State.AWAITING_SEXTORTION_VIOLATION:
            if message.content.lower() in self.YES_KEYWORDS:
                offender_id = self.handling_report.message.author.id
                self.client.banned_users.add(offender_id)
                self.state = State.AWAITING_ADDITIONAL_DATA_COLLECTION_CONFIRM

                other_reports = [
                    report.id
                    for report in self.client.open_reports
                    if report.message.author.id == offender_id
                    and report.id != self.handling_report.id
                ]

                response = [
                    ModerateMessage.BANNED_USER.format(
                        author=self.handling_report.message.author.name
                    )
                ]

                if other_reports:
                    response.append(
                        ModerateMessage.ADDITIONAL_DATA_COLLECTION.format(
                            reports="\n" + "\n".join(["- " + r for r in other_reports])
                        )
                    )
                else:
                    response.append(
                        ModerateMessage.ADDITIONAL_DATA_COLLECTION_NO_REPORTS
                    )

                return response
            elif message.content.lower() in self.NO_KEYWORDS:
                other_reports = [
                    report.id
                    for report in self.client.open_reports
                    if report.reporter.id == self.handling_report.reporter.id
                    and report.id != self.handling_report.id
                ]

                if other_reports:
                    self.state = State.AWAITING_ADVERSARIAL_REPORTING
                    return ModerateMessage.ADVERSARIAL_REPORTING.format(
                        reports="\n" + "\n".join(["- " + r for r in other_reports])
                    )

                self.state = State.MODERATE_COMPLETE
                self.client.open_reports.remove(self.handling_report)
                return ModerateMessage.ADVERSARIAL_REPORTING_NO_COMPLETE
            else:
                return GenericMessage.INVALID_YES_NO

        if self.state == State.AWAITING_ADDITIONAL_DATA_COLLECTION_CONFIRM:
            if message.content.lower() in self.YES_KEYWORDS:
                self.state = State.MODERATE_COMPLETE
                self.client.open_reports.remove(self.handling_report)
                return ModerateMessage.YES_ESCALATE
            elif message.content.lower() in self.NO_KEYWORDS:
                self.state = State.MODERATE_COMPLETE
                return ModerateMessage.NO_ESCALATE
            else:
                return GenericMessage.INVALID_YES_NO

        if self.state == State.AWAITING_ADVERSARIAL_REPORTING:
            if message.content.lower() in self.YES_KEYWORDS:
                self.state = State.MODERATE_COMPLETE
                self.client.open_reports.remove(self.handling_report)
                self.client.banned_users.add(self.handling_report.reporter.id)
                return [
                    ModerateMessage.TEMP_BANNED_USER.format(
                        author=self.handling_report.reporter.name, days=7
                    ),
                    ModerateMessage.YES_ESCALATE,
                ]
            elif message.content.lower() in self.NO_KEYWORDS:
                self.state = State.MODERATE_COMPLETE
                self.client.open_reports.remove(self.handling_report)
                return ModerateMessage.ADVERSARIAL_REPORTING_NO_COMPLETE
            else:
                return GenericMessage.INVALID_YES_NO

        return []

    def moderation_complete(self):
        return self.state == State.MODERATE_COMPLETE
