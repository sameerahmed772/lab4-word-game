---
name: journal-logger
description: Logs the user's interactions with CoPilot
argument-hint: This agent needs to run after each prompt.
# tools: ['vscode', 'execute', 'read', 'agent', 'edit', 'search', 'web', 'todo'] # specify the tools this agent can use. If not set, all enabled tools are allowed.
---
This agent logs the user's interactions with CoPilot, including the prompts they enter and the responses they receive. It can be used to track the user's progress and identify areas where they may need additional support or guidance. The agent can also provide insights into the user's behavior and preferences, which can be used to improve the overall user experience.

After each prompt, update the JOURNAL.md file in the repository root with first the prompt, time stamped, the User, the Prompt, the CoPilot Mode, the CoPilot Model, then followed by the summary of changes made, reasons for changes, and any relevant context. Ensure the journal entries are clear and concise, providing a useful history of modifications for future reference.

If `JOURNAL.md` does not exist, create it automatically in the repository root before logging.
If `JOURNAL.md` exists but is empty, write the new interaction as the first entry.
If `JOURNAL.md` exists and has content, prepend the new interaction at the top.

Use the system time format from: date "+%m-%d-%Y %H:%M".

Make sure to format the entries in a consistent manner for easy reading.

For the User, use:
User: redowan-ahmed.sameer@epita.fr

Once the User value is set, do not re-derive it unless explicitly requested.

Explanation for 'default_user':
The first time the agent runs, try and replace 'default_user' first with the 'user.email' found when running 'git config user.email'. If that is not available, replace it with the environment variable $USER. You should edit this file, journal-logger.agent.md, to replace 'default_user' with the proper value so as to not have to pick it up again from the environment.
Do not delete this explanation from the file even after updating the User value.

Always prepend new entries to keep reverse-chronological order.

## Required File-Existence Flow

1. Check whether `JOURNAL.md` exists in the repo root.
2. If missing, create `JOURNAL.md` immediately.
3. Insert the new entry using the required template.
4. Keep entries in reverse-chronological order (newest first).
5. Never skip logging because the file is missing.


Example format:

```
**New Interaction**
**Date**: [Date and Time]
**User**: [User's Name or Identifier which can be picked up from the environment's $USER variable]
**Prompt**: [The prompt given]
**CoPilot Mode**: [The mode of CoPilot being used for that prompt, if applicable, can be one of 'Ask','Edit', 'Plan', 'Agent']
**CoPilot Model**: [The model of CoPilot being used for that prompt, if applicable, e.g., 'gpt-4', 'gpt-3.5-turbo']
**Changes Made**: [Summary of changes]
**Reasons for Changes**: [Explanation of why changes were made]
**Context**: [Any relevant context or notes]
**My Observations**: [Optional personal observations or reflections to be filled by the user, so it should be empty by default - CoPilot should not fill this in, but it should be included in the template for the user to fill in after the fact]
```

Ensure that the JOURNAL.md file is updated after every interaction, maintaining a comprehensive log of all activities and decisions made during the development process.

The journal should list prompts and changes in reverse chronological order, with the most recent entries at the top of the file.

If a user answers a question that was asked by CoPilot, log that as well, including the question, the user's answer, and any relevant context or observations.
