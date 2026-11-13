
import { useRef, useState } from "react";
import {
    uploadDocument,
    searchKnowledge,
    askKnowledge,
} from "../services/api";

import "./KnowledgeHubPage.css";


function KnowledgeHubPage() {
    const fileInputRef = useRef(null);

    const [selectedFile, setSelectedFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [uploadResult, setUploadResult] = useState(null);
    const [uploadError, setUploadError] = useState("");

    const [searchQuery, setSearchQuery] = useState("");
    const [searching, setSearching] = useState(false);
    const [searchResults, setSearchResults] = useState(null);
    const [searchError, setSearchError] = useState("");

    const [question, setQuestion] = useState("");
    const [asking, setAsking] = useState(false);
    const [aiResponse, setAiResponse] = useState(null);
    const [aiError, setAiError] = useState("");

    const [topK, setTopK] = useState(3);


    // Handle PDF selection
    function handleFileChange(event) {
        const file = event.target.files?.[0];

        setUploadError("");
        setUploadResult(null);

        if (!file) {
            setSelectedFile(null);
            return;
        }

        if (!file.name.toLowerCase().endsWith(".pdf")) {
            setSelectedFile(null);
            setUploadError("Please select a PDF file.");
            event.target.value = "";
            return;
        }

        if (file.size > 10 * 1024 * 1024) {
            setSelectedFile(null);
            setUploadError("File size must not exceed 10 MB.");
            event.target.value = "";
            return;
        }

        setSelectedFile(file);
    }


    // Upload PDF document
    async function handleUpload(event) {
        event.preventDefault();

        if (!selectedFile) {
            setUploadError("Please select a PDF document first.");
            return;
        }

        setUploading(true);
        setUploadError("");
        setUploadResult(null);

        try {
            const result = await uploadDocument(selectedFile);

            setUploadResult(result);
            setSelectedFile(null);

            if (fileInputRef.current) {
                fileInputRef.current.value = "";
            }

        } catch (error) {
            setUploadError(error.message);
        } finally {
            setUploading(false);
        }
    }


    // Search enterprise knowledge
    async function handleSearch(event) {
        event.preventDefault();

        if (searchQuery.trim().length < 3) {
            setSearchError("Enter at least 3 characters to search.");
            return;
        }

        setSearching(true);
        setSearchError("");
        setSearchResults(null);

        try {
            const result = await searchKnowledge(
                searchQuery.trim(),
                topK
            );

            setSearchResults(result);

        } catch (error) {
            setSearchError(error.message);
        } finally {
            setSearching(false);
        }
    }


    // Ask Knowledge AI
    async function handleAskAI(event) {
        event.preventDefault();

        if (question.trim().length < 3) {
            setAiError("Please enter a question with at least 3 characters.");
            return;
        }

        setAsking(true);
        setAiError("");
        setAiResponse(null);

        try {
            const result = await askKnowledge(
                question.trim(),
                topK
            );

            setAiResponse(result);

        } catch (error) {
            setAiError(error.message);
        } finally {
            setAsking(false);
        }
    }


    function formatFileSize(bytes) {
        if (!bytes) return "0 KB";

        return `${(bytes / 1024).toFixed(1)} KB`;
    }


    return (
        <div className="knowledge-page">

            {/* Page Heading */}
            <section className="knowledge-header">

                <div>
                    <div className="knowledge-eyebrow">
                        ENTERPRISE KNOWLEDGE MANAGEMENT
                    </div>

                    <h1>Knowledge Hub</h1>

                    <p>
                        Upload enterprise documents, discover relevant information
                        and get AI-powered answers grounded in your knowledge base.
                    </p>
                </div>

                <div className="knowledge-header-icon">
                    ◈
                </div>

            </section>


            {/* Knowledge Metrics */}
            <section className="knowledge-metrics">

                <div className="knowledge-metric-card">
                    <div className="knowledge-metric-icon blue-icon">
                        ▧
                    </div>

                    <div>
                        <span>Latest Upload</span>

                        <h3>
                            {uploadResult
                                ? uploadResult.original_filename
                                : "No upload yet"}
                        </h3>

                        <p>Current session</p>
                    </div>
                </div>


                <div className="knowledge-metric-card">
                    <div className="knowledge-metric-icon purple-icon">
                        ◫
                    </div>

                    <div>
                        <span>Pages Processed</span>

                        <h3>
                            {uploadResult
                                ? uploadResult.total_pages_extracted
                                : "—"}
                        </h3>

                        <p>Latest uploaded PDF</p>
                    </div>
                </div>


                <div className="knowledge-metric-card">
                    <div className="knowledge-metric-icon green-icon">
                        ◈
                    </div>

                    <div>
                        <span>Knowledge Chunks</span>

                        <h3>
                            {uploadResult
                                ? uploadResult.total_chunks_in_knowledge_base
                                : "—"}
                        </h3>

                        <p>Total indexed chunks</p>
                    </div>
                </div>


                <div className="knowledge-metric-card">
                    <div className="knowledge-metric-icon orange-icon">
                        ✧
                    </div>

                    <div>
                        <span>AI Engine</span>
                        <h3>Ollama</h3>
                        <p>Local LLM processing</p>
                    </div>
                </div>

            </section>


            {/* Upload Section */}
            <section className="knowledge-panel upload-panel">

                <div className="knowledge-panel-heading">

                    <div className="knowledge-heading-icon">
                        ↑
                    </div>

                    <div>
                        <h2>Upload Documents</h2>

                        <p>
                            Add PDF documents to your enterprise knowledge base.
                        </p>
                    </div>

                </div>


                <form onSubmit={handleUpload}>

                    <div
                        className="upload-dropzone"
                        onClick={() => fileInputRef.current?.click()}
                        onDragOver={(event) => event.preventDefault()}
                        onDrop={(event) => {
                            event.preventDefault();

                            const file = event.dataTransfer.files?.[0];

                            if (file) {
                                handleFileChange({
                                    target: {
                                        files: [file],
                                        value: "",
                                    },
                                });
                            }
                        }}
                    >

                        <input
                            ref={fileInputRef}
                            type="file"
                            accept=".pdf,application/pdf"
                            onChange={handleFileChange}
                            hidden
                        />

                        <div className="upload-cloud-icon">
                            ⇧
                        </div>

                        <h3>
                            {selectedFile
                                ? selectedFile.name
                                : "Drop your PDF here"}
                        </h3>

                        <p>
                            {selectedFile
                                ? formatFileSize(selectedFile.size)
                                : "or click to browse files"}
                        </p>

                        <span className="upload-file-info">
                            PDF files only · Maximum file size 10 MB
                        </span>

                    </div>


                    {uploadError && (
                        <div className="knowledge-alert error-alert">
                            ⚠ {uploadError}
                        </div>
                    )}


                    {uploadResult && (
                        <div className="knowledge-alert success-alert">

                            <strong>✓ Document processed successfully!</strong>

                            <p>
                                {uploadResult.original_filename} was added to
                                your knowledge base.
                            </p>

                            <div className="upload-result-stats">
                                <span>
                                    {uploadResult.total_pages_extracted} pages
                                </span>

                                <span>
                                    {uploadResult.total_chunks_created} chunks created
                                </span>

                                <span>
                                    {uploadResult.total_chunks_stored} chunks stored
                                </span>
                            </div>

                        </div>
                    )}


                    <div className="upload-actions">

                        <button
                            type="button"
                            className="secondary-button"
                            onClick={() => {
                                setSelectedFile(null);
                                setUploadError("");
                                setUploadResult(null);

                                if (fileInputRef.current) {
                                    fileInputRef.current.value = "";
                                }
                            }}
                            disabled={uploading}
                        >
                            Clear
                        </button>

                        <button
                            type="submit"
                            className="knowledge-primary-button"
                            disabled={!selectedFile || uploading}
                        >
                            {uploading
                                ? "Processing PDF..."
                                : "Upload & Process PDF"}
                        </button>

                    </div>

                </form>

            </section>


            {/* Semantic Search */}
            <section className="knowledge-panel">

                <div className="knowledge-panel-heading">

                    <div className="knowledge-heading-icon search-icon">
                        ⌕
                    </div>

                    <div>
                        <h2>Semantic Knowledge Search</h2>

                        <p>
                            Find relevant information across your indexed documents.
                        </p>
                    </div>

                </div>


                <form
                    className="knowledge-search-form"
                    onSubmit={handleSearch}
                >

                    <div className="knowledge-search-input">
                        <span>⌕</span>

                        <input
                            type="text"
                            placeholder="Search payment failures, AWS, company policies..."
                            value={searchQuery}
                            onChange={(event) => setSearchQuery(event.target.value)}
                        />
                    </div>


                    <select
                        value={topK}
                        onChange={(event) => setTopK(Number(event.target.value))}
                        aria-label="Number of search results"
                    >
                        <option value={3}>Top 3</option>
                        <option value={5}>Top 5</option>
                        <option value={10}>Top 10</option>
                    </select>


                    <button
                        type="submit"
                        className="knowledge-primary-button"
                        disabled={searching}
                    >
                        {searching ? "Searching..." : "Search"}
                    </button>

                </form>


                {searchError && (
                    <div className="knowledge-alert error-alert">
                        ⚠ {searchError}
                    </div>
                )}


                {searchResults && (
                    <div className="knowledge-results">

                        <div className="results-heading">
                            <h3>Search Results</h3>

                            <span>
                                {searchResults.results_found} results found
                            </span>
                        </div>


                        {searchResults.results.length === 0 ? (
                            <div className="empty-knowledge-state">
                                No matching document chunks were found.
                            </div>
                        ) : (
                            searchResults.results.map((result, index) => (
                                <div
                                    className="knowledge-result-card"
                                    key={`${result.source}-${result.page_number}-${index}`}
                                >

                                    <div className="result-card-top">

                                        <span className="result-number">
                                            Source {index + 1}
                                        </span>

                                        <span className="result-page">
                                            Page {result.page_number}
                                        </span>

                                    </div>

                                    <h4>{result.source}</h4>

                                    <p>{result.content}</p>

                                    <span className="result-distance">
                                        Retrieval distance:{" "}
                                        {Number(result.distance).toFixed(4)}
                                    </span>

                                </div>
                            ))
                        )}

                    </div>
                )}

            </section>


            {/* AI Question Answering */}
            <section className="knowledge-panel ai-knowledge-panel">

                <div className="knowledge-panel-heading">

                    <div className="knowledge-heading-icon ai-heading-icon">
                        ✧
                    </div>

                    <div>
                        <h2>Ask Knowledge AI</h2>

                        <p>
                            Get answers generated from your enterprise documents
                            using Retrieval-Augmented Generation.
                        </p>
                    </div>

                </div>


                <form onSubmit={handleAskAI}>

                    <textarea
                        className="knowledge-question-input"
                        placeholder="Ask something about your enterprise documents...&#10;&#10;Example: What are the common causes of payment failures?"
                        value={question}
                        onChange={(event) => setQuestion(event.target.value)}
                        rows={4}
                    />


                    <div className="ai-question-footer">

                        <span>
                            ✧ Powered by ChromaDB + Ollama
                        </span>

                        <button
                            type="submit"
                            className="knowledge-primary-button"
                            disabled={asking}
                        >
                            {asking
                                ? "Generating Answer..."
                                : "Ask Knowledge AI →"}
                        </button>

                    </div>

                </form>


                {aiError && (
                    <div className="knowledge-alert error-alert">
                        ⚠ {aiError}
                    </div>
                )}


                {aiResponse && (
                    <div className="ai-answer-container">

                        <div className="ai-answer-heading">

                            <div className="ai-answer-icon">
                                ✧
                            </div>

                            <div>
                                <h3>AI Generated Answer</h3>

                                <span className={`answer-status ${aiResponse.status}`}>
                                    {aiResponse.status.replaceAll("_", " ")}
                                </span>
                            </div>

                        </div>


                        <div className="ai-answer-content">
                            {aiResponse.answer}
                        </div>


                        {aiResponse.sources?.length > 0 && (
                            <div className="ai-sources">

                                <h4>Knowledge Sources</h4>

                                <div className="ai-source-list">

                                    {aiResponse.sources.map((source, index) => (
                                        <div
                                            className="ai-source-item"
                                            key={`${source.filename}-${source.page_number}-${index}`}
                                        >

                                            <span className="source-file-icon">
                                                ▧
                                            </span>

                                            <div>
                                                <strong>
                                                    Source {source.source_number ?? index + 1}
                                                </strong>

                                                <p>{source.filename}</p>
                                            </div>

                                            <span className="source-page">
                                                Page {source.page_number}
                                            </span>

                                        </div>
                                    ))}

                                </div>

                            </div>
                        )}


                        {aiResponse.citation_status && (
                            <div className="citation-info">
                                Citation status:{" "}
                                <strong>
                                    {aiResponse.citation_status.replaceAll("_", " ")}
                                </strong>
                            </div>
                        )}


                        <div className="ai-disclaimer">
                            AI-generated responses are advisory. Verify important
                            information against the original enterprise records
                            and documentation.
                        </div>

                    </div>
                )}

            </section>


            {/* Footer */}
            <footer className="knowledge-footer">
                <span>EnterpriseBrain 360</span>

                <span>
                    Local-first enterprise knowledge intelligence
                </span>
            </footer>

        </div>
    );
}


export default KnowledgeHubPage;
