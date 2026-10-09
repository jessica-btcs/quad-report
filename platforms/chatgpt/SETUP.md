# Quad Report in ChatGPT: setup (about 5 minutes)

You set this up once, as a ChatGPT Project. It is private to your account.

1. **Turn off model training on your chats.** In ChatGPT, open
   **Settings > Data controls** and turn off **Improve the model for
   everyone**. You will be uploading your financials.
2. **Create the Project.** In the sidebar, click **New project** and name it
   `Quad Report`.
3. **Add the instructions.** Open the Project's settings (the ⋯ next to its
   name), find **Instructions**, and paste in everything from
   `project-instructions.txt` in this folder.
4. **Add the files.** In the Project, click **Add files** and upload every
   file in the `files` folder here ({count} files). Wait until they have all
   finished.
5. **Test it.** Start a chat inside the Project and say
   `Show me the sample slide`. You should get a PowerPoint file back.
6. **Start setup.** Say `set up my quad report`. At the end it hands you
   `quad-profile.json`. Save it into your Quad Report Data folder.

## Every month

Open a chat inside the Quad Report Project and say
`build my quad for September`. Attach your profile and last month's history
file when it asks, and save what it hands back into your folder.

## When an update arrives

Delete the old files from the Project, upload the new `files` folder, and
paste in the new `project-instructions.txt`. Your Quad Report Data folder is
never touched.

## Using the ChatGPT desktop app or Codex instead?

You can install it as a plugin that updates from the source: add the
marketplace `jessica-btcs/quad-report` in the app's Plugins page, or run
`codex plugin marketplace add jessica-btcs/quad-report`, then install
**quad-report**.
