class GenericMessage:
    INVALID_YES_NO = "I'm sorry, I didn't understand that. Please type `yes` or `no`."
    INVALID_RESPONSE = (
        "I'm sorry, I didn't understand that. Please try again or type `cancel` to"
        " cancel."
    )
    INVALID_REACTION = (
        "I'm sorry, I didn't understand that reaction. Please try again or type"
        " `cancel` to cancel the report."
    )
    CANCELED = "Report canceled."
    REPORT_COMPLETE = (
        "Thank you for reporting this activity. Our moderation team will review your"
        " report and contact you if needed. No further action is required on your part."
    )
    INVALID_SKIP = (
        "I'm sorry. This question cannot be skipped. Please choose an option or type"
        " `cancel` to cancel the report."
    )
    INVALID_NUMBER = (
        "I'm sorry, I didn't understand that number. Please try again or type `cancel`"
        " to cancel the report."
    )
    BANNED_USER = "You are currently banned."
    BANNED_OTHER_USER = (
        "That user is already banned. If this was a mistake, please try again or type"
        " `cancel` to cancel the report."
    )


class ReportStartMessage:
    START = (
        "Thank you for starting the reporting process. Type `help` at any time for more"
        " information or `cancel` to cancel the report."
    )
    REQUEST_MSG = (
        "Please copy paste the link to the message you want to report.\nYou can obtain"
        " this link by right-clicking the message and clicking `Copy Message Link`."
    )
    MODERATE_REQUEST = "Please type the report id of the report you want to handle."
    INVALID_LINK = (
        "I'm sorry, I couldn't read that link. Please try again or type `cancel` to"
        " cancel."
    )
    INVALID_REPORTID = (
        "I'm sorry there is no open report associated with that report id. Please try"
        " again or type `cancel` to cancel."
    )
    NOT_IN_GUILD = (
        "I cannot accept reports of messages from guilds that I'm not in. Please have"
        " the guild owner add me to the guild and try again."
    )
    CHANNEL_DELETED = (
        "It seems this channel was deleted or never existed. Please try again or type"
        " `cancel` to cancel the report."
    )
    MESSAGE_DELETED = (
        "It seems this message was deleted or never existed. Please try again or type"
        " `cancel` to cancel the report."
    )
    MESSAGE_IDENTIFIED = (
        "I found this message:\n```{author}: {content}```\nIs"
        " this the message you want to report? Please type `yes` or `no`."
    )
    MESSAGE_IDENTIFIED_ATTACHMENTS = (
        "I found this message:\n```{author}: {content}```*Includes {num_attachments}"
        " attachment(s).*\n{attachments}\n\nIs this the message you want to report?"
        " Please type `yes` or `no`."
    )
    REPORT_IDENTIFIED = (
        "I found this report:\n```{report_id}: {content}```\nIs"
        " this the report you want to handle? Please type `yes` or `no`."
    )


class UserDetailsMessage:
    ON_BEHALF_OF = (
        "Are you reporting on behalf of someone else? Please type `yes` or `no`."
    )
    WHO_ON_BEHALF_OF = "Who are you reporting on behalf of?"


class ReportDetailsMessage:
    REASON_FOR_REPORT = (
        "Please select the reason for reporting this message. React to this message"
        " with the corresponding emoji.\n1️⃣ - Harassment or offensive content \n2️⃣ - Spam"
        " \n3️⃣ - Immediate danger\n4️⃣ - Other"
    )
    ABUSE_TYPE = (
        "What type of abuse are you reporting? React to this message with the"
        " corresponding emoji.\n1️⃣ - Sexually explicit harassment\n2️⃣ - Encouraging"
        " self-harm\n3️⃣ - Hate speech\n4️⃣ - Other"
    )
    ABUSE_DESCRIPTION = (
        "Which of the following best describes the situation? React to this message"
        " with the corresponding emoji.\n1️⃣ - The reporting user is receiving sexually"
        " explicit content (images, text)\n2️⃣ - The reporting user is receiving unwanted"
        " requests involving sexually explicit content"
    )
    UNWANTED_REQUESTS = (
        "What is the account you are reporting requesting? React to this"
        " message with the corresponding emoji.\n1️⃣ - Money\n"
        "2️⃣ - Additional sexually explicit content\n3️⃣ - Other"
    )
    MULTIPLE_REQUESTS = (
        "Have you or the person on behalf of whom this report is being filed received"
        " multiple requests from the account you are reporting? Please type `yes` or"
        " `no`."
    )
    APPROXIMATE_REQUESTS = "Please approximate the number of requests."
    COMPLIED_WITH_REQUESTS = (
        "Have you or the person on behalf of whom this report is being filed complied"
        " with these requests? Please type `yes` or `no`."
    )
    MINOR_PARTICIPATION = (
        "Does the sexually explicit content involve a minor? Please type `yes` or `no`."
    )
    CONTAIN_YOURSELF = (
        "Does this content contain you or the person on behalf of whom this report is"
        " being filed? Please type `yes` or `no`."
    )
    ENCOURAGE_SELF_HARM = (
        "Is the account you are reporting encouraging self-harm? Please type `yes`,"
        " `no`, or `skip` to skip this question."
    )
    SELF_HELP_RESOURCES = (
        "Please know that there are many resources available to you if you are"
        " struggling with self-harm or suicidal thoughts. Please contact one of the"
        " following helplines as they will be able to provide you with immediate"
        " support and resources:\n- Emergency: 911\n- Self-Harm Hotline: 1-800-DONT-CUT"
        " (1-800-366-8288)\n- Crisis Text Line: Text 'HOME' to 741741 or"
        " <https://connect.crisistextline.org/chat>\n- National Suicide Prevention"
        " Lifeline: 1-800-273-TALK (8255) or"
        " <https://suicidepreventionlifeline.org/chat/>"
    )
    ADDITIONAL_INFO = (
        "Would you like to provide any additional information? Please type `yes` or"
        " `no`."
    )
    PLEASE_SPECIFY = "Please specify."
    BLOCK_USER = (
        "Would you like to block the account you have reported? Please type `yes` or"
        " `no`."
    )
    BLOCKED = "`{author}` has been blocked."
    CONFIRMATION = (
        "Here is a summary of your report. Please type `yes` or `no` to confirm that"
        " you would like to submit this report."
    )


class ModerateMessage:
    START = "Moderating flow has started."
    IS_SEXTORTION_VIOLATION = (
        "Does this message fall into the category of non-consenual intimate imagery or"
        " sextortion as outlined in our community guidelines? Answering `yes` will"
        " permanently ban the user from our platform."
    )
    BANNED_USER = "`{author}` has been banned."
    ADDITIONAL_DATA_COLLECTION_NO_REPORTS = (
        "There are no other reports filed against this user. Please type `yes` or"
        " `no` to confirm that you would like to transfer this report to a higher-level"
        " moderator that may take further action."
    )

    ADDITIONAL_DATA_COLLECTION = (
        "Here are other reports filed against this user:{reports}\nAfter reviewing"
        " these reports, please type `yes` or `no` to confirm that you would like to"
        " transfer this report to a higher-level moderator that may take further"
        " action."
    )

    NO_ESCALATE = (
        "No further action is required on your part. This report will stay on file."
    )
    YES_ESCALATE = (
        "Thank you for reviewing this report. This activity and associated reports will"
        " be sent to another team for further investigation."
    )

    ADVERSARIAL_REPORTING = (
        "Here are other reports filed by this user:{reports}\nAfter reviewing"
        " these reports, please type `yes` or `no` to confirm that this user is"
        " participating in adversarial reporting."
    )

    TEMP_BANNED_USER = "`{author}` has been temporarily banned for {days} day(s)."

    ADVERSARIAL_REPORTING_NO_COMPLETE = (
        "Thank you for reviewing this report. No further action is required on your"
        " part."
    )
