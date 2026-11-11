# Reviewing solicitation documents by relevant section

**Elias Brown · Document parsing, AI summarization, React, and integration · Team capstone**

Requests for information and proposals can contain long documents whose relevant requirements are spread across many sections. This capstone developed a review application that accepts a document, identifies sections relevant to an organization’s capabilities, and presents concise summaries that a person can review.

My work covered document parsing, prompts and summarization, the frontend, and integration. I worked with **Kayla Stevenson, Timothy Poteet, and Wyatt Phillips**; backend and database responsibilities were handled by my teammates. The application described here is the team’s solution.

## Follow the document through a review workflow

The implementation connects PDF and Word-document parsing to section selection and summarization. It provides progress updates while processing and stores the resulting summaries for later retrieval. The frontend supports browsing and searching saved results and managing individual records.

<figure class="workflow"><ol class="process-flow"><li><span class="step-label">01</span><strong>Parse</strong><span>Convert a document to structured text.</span></li><li><span class="step-label">02</span><strong>Select</strong><span>Identify sections relevant to the review.</span></li><li><span class="step-label">03</span><strong>Summarize</strong><span>Condense selected sections into bullets.</span></li><li><span class="step-label">04</span><strong>Review</strong><span>Browse, search, and manage saved summaries.</span></li></ol><figcaption>A simplified view of the team application. This diagram contains no client documents or generated client summaries.</figcaption></figure>

The deliverable is an integrated document-review workflow. The repository provides evidence of that implementation, but this report does not claim a measured reduction in review time, classification accuracy, or commercial success.

## My contribution

| Area | My work |
|---|---|
| Document parsing | Developed the document-to-text workflow and the instructions used to preserve useful structure |
| Section selection and summarization | Developed the prompts and processing sequence for identifying relevant material and condensing it |
| Frontend | Developed the upload, progress, results, and saved-summary interfaces |
| Integration | Connected the document-processing workflow and user interface with the team’s backend and persistence layer |

My teammates handled backend and database development. This distinction matters because the application’s behavior depends on all of those parts working together.

## Select before summarizing

The processing sequence first interprets document headings and groups text into sections. It then evaluates relevance using a section’s heading and an initial excerpt, with an organization-specific capability description as context. Relevant sections are split when needed, summarized, and condensed into a small number of bullets.

This choice focuses the output on material selected for review. It also creates an important limitation: a section excluded at the relevance stage does not appear in the final summary. The selection step therefore deserves as much attention as the quality of the summary text.

[Read the processing methods and limits](docs/METHODS.md)

## Make processing and saved results understandable

The frontend exposes the stages of processing so that a user can distinguish parsing, section analysis, and saving. A saved result retains its filename, upload time, and section summaries. Users can search saved records and return to a particular result.

The interface also checks whether a filename already exists before processing a new upload. That check supports a user decision about a possible repeat submission; it is not a content-based duplicate detector.

## Evidence and scope

The [public source repository](https://github.com/eliasbrown99/Capstone) contains the parsing, summarization, service, and interface implementation. This reading edition describes the source as reviewed; the application was not executed and no documents were sent to a parsing or model service to produce the report.

No client documents, client-generated summaries, or organization-specific capability statements are reproduced here. The report does not invent a demonstration result or treat a generated summary as a complete review of the original solicitation.
