# How the document-review workflow selects and summarizes material

**Methods and limits · A source-based account of the team implementation**

The application combines a document parser, several language-model steps, a backend, a database, and a review interface. Each stage changes the representation of the input, so a useful account needs to identify both what it produces and what it can leave out.

## Parse document structure

The parsing component accepts PDF and Word documents and uses a document-parsing service to produce Markdown-like text. Its instructions emphasize headings, narrative text, lists, and tables while attempting to remove repeated document furniture such as titles or tables of contents.

The summarization component then finds heading lines and asks a language model whether they represent numbered or Roman-numeral sections. Headings that do not pass that check are treated as body text. The retained boundaries form a flat list of sections rather than a full nested document hierarchy.

That is a deliberate representation of the document, not a guarantee that all source formatting is preserved. Unnumbered sections and ambiguous heading styles can affect where one section ends and another begins. [Parsing source](https://github.com/eliasbrown99/Capstone/blob/c8105f820f062c6097f1a0a2d39d11cdb0bffb4e/app/parser.py) · [Section-processing source](https://github.com/eliasbrown99/Capstone/blob/c8105f820f062c6097f1a0a2d39d11cdb0bffb4e/app/summarization.py).

## Make a relevance decision

For each section, the implementation sends its heading and the first 1,000 characters of text to a relevance-classification step. An organization-specific capability description supplies the context. The reviewed code processes only sections that this step marks relevant.

The excerpt keeps the selection input bounded. It can also miss a requirement that appears later in a long section. This means the result should be understood as a selected digest, not evidence that all requirements in the solicitation have been captured.

The public report describes the mechanism without reproducing the organization-specific capability text or treating it as an independently verified description of that organization.

## Summarize selected sections

Relevant sections are divided into text chunks using a configured size of 2,000 characters with 100 characters of overlap. Each chunk is summarized, the partial outputs are combined, and a final prompt requests no more than five bullets for the section.

These settings describe the existing implementation. They are not presented as experimentally selected optimum values. The chunking and compression steps can lose context or omit detail, and a prompt instruction about length is not a measure of factual completeness.

| Stage | Output | Question for evaluation |
|---|---|---|
| Parsing | Extracted document text | Were tables, conditions, and headings retained accurately? |
| Section construction | Flat sections | Do the boundaries preserve the intended context? |
| Relevance selection | Sections selected for summarization | Were important requirements excluded? |
| Summarization | Concise bullets by section | Are the bullets faithful, complete enough, and free of added claims? |
| User review | A saved digest | Can the reviewer confirm important statements against the source? |

This report does not include an independently labeled evaluation set or performance estimate for those stages.

## Connect processing to the application

The backend provides an upload-processing route that streams progress messages and the final result. The database stores the filename, upload time, and structured summary payload. Additional routes retrieve, search, and delete saved summaries and check whether a filename is already present.

The frontend uses those interfaces for the upload and review experience. My contribution covered parsing, prompts and summarization, frontend behavior, and integration; the backend and database were developed by teammates. [Backend source](https://github.com/eliasbrown99/Capstone/blob/c8105f820f062c6097f1a0a2d39d11cdb0bffb4e/app/main.py) · [Database source](https://github.com/eliasbrown99/Capstone/blob/c8105f820f062c6097f1a0a2d39d11cdb0bffb4e/app/database.py).

## Keep the claims at the level supported by the work

The reviewed implementation supports a clear account of the processing sequence and application features. It does not establish accuracy on unseen solicitations, the absence of omitted requirements, or improved business decisions. The saved summary fields retain section headings and text, but do not provide page-level source citations.

The report therefore presents the application as a capstone review tool. It preserves the technical choices and their implications without implying that generated summaries replace reading and evaluating the original document.

[Return to the project overview](../README.md)
