import { useState, useRef, useEffect } from "react";
import "./App.css";
import avatarImg from "./assets/avatar.png";

const EMAIL_REGEX = /^[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}$/;
const PHONE_REGEX = /^\+[1-9]\d{6,14}$/;

const COUNTRY_CODES = [
  { code: "+91", name: "India", minDigits: 10, maxDigits: 10 },
  { code: "+98", name: "Iran", minDigits: 10, maxDigits: 10 },
  { code: "+971", name: "UAE", minDigits: 9, maxDigits: 9 },
  { code: "+966", name: "Saudi Arabia", minDigits: 9, maxDigits: 9 },
  { code: "+974", name: "Qatar", minDigits: 8, maxDigits: 8 },
  { code: "+965", name: "Kuwait", minDigits: 8, maxDigits: 8 },
  { code: "+92", name: "Pakistan", minDigits: 10, maxDigits: 10 },
  { code: "+880", name: "Bangladesh", minDigits: 10, maxDigits: 10 },
  { code: "+1", name: "USA / Canada", minDigits: 10, maxDigits: 10 },
  { code: "+44", name: "United Kingdom", minDigits: 9, maxDigits: 10 },
  { code: "+61", name: "Australia", minDigits: 9, maxDigits: 9 },
  { code: "+90", name: "Turkey", minDigits: 10, maxDigits: 10 },
  { code: "+20", name: "Egypt", minDigits: 10, maxDigits: 10 },
  { code: "+86", name: "China", minDigits: 11, maxDigits: 11 },
  { code: "+81", name: "Japan", minDigits: 10, maxDigits: 10 },
];

const SERVICE_OPTIONS = [
  "Electrical Safety Testing",
  "EMC/EMI Testing",
  "Electro-Medical Equipment",
  "Photometry (LM-79/LM-80)",
  "Environmental / IP Testing",
  "Calibration Services",
  "Packaging Testing",
  "Software Testing",
  "Information Security",
];

const CALLBACK_OPTIONS = [
  "As soon as possible",
  "Today (Afternoon)",
  "Tomorrow Morning",
  "Tomorrow Afternoon",
];


const ServiceTable = ({ tableData }) => {
  if (!tableData || !tableData.data || !Array.isArray(tableData.data) || tableData.data.length === 0) return null;
  
  const columns = Object.keys(tableData.data[0]);
  
  return (
    <div className="service-table-container">
      <div className="service-table-header">
        {tableData.title || "Details"}
      </div>
      <table className="service-table">
        <tbody>
          {tableData.data.map((row, i) => (
            <tr key={i} className={i % 2 === 0 ? 'row-even' : 'row-odd'}>
              {columns.map((col, j) => (
                <td key={j}>{row[col]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

const MessageContent = ({ content, isHighlighted, activeCharIndex }) => {
  if (!isHighlighted) {
    return content.split("\n").map((line, i) => {
      if (!line) return <p key={i} className="empty-line"><br /></p>;
      
      return (
        <p key={i}>
          {line.split(/(\*\*.*?\*\*)/g).map((part, j) =>
            part.startsWith("**") && part.endsWith("**") ? (
              <strong key={j}>{part.slice(2, -2)}</strong>
            ) : (
              part
            )
          )}
        </p>
      );
    });
  }

  let currentOffset = 0;
  return content.split("\n").map((line, i) => {
    const lineStart = currentOffset;
    const lineEnd = currentOffset + line.length;
    currentOffset = lineEnd + 1; // +1 for the \n we split by

    // Split line into sentences (including trailing punctuation/spaces)
    const regex = /([^.!?]+[.!?]*)/g;
    const sentences = [];
    let match;
    while ((match = regex.exec(line)) !== null) {
      sentences.push({
        text: match[0],
        start: lineStart + match.index,
        end: lineStart + match.index + match[0].length
      });
    }

    if (sentences.length === 0) {
      return <p key={i}><br /></p>;
    }

    return (
      <p key={i}>
        {sentences.map((sentence, idx) => {
          const active = activeCharIndex >= sentence.start && activeCharIndex < sentence.end;
          const className = active ? "highlighted-sentence" : "";

          return (
            <span key={idx} className={className}>
              {sentence.text.split(/(\*\*.*?\*\*)/g).map((part, j) =>
                part.startsWith("**") && part.endsWith("**") ? (
                  <strong key={j}>{part.slice(2, -2)}</strong>
                ) : (
                  part
                )
              )}
            </span>
          );
        })}
      </p>
    );
  });
};

function EnquiryForm({ formData, formErrors, loading, onChange, onSubmit, onCancel, nameInputRef }) {
  return (
    <form
      className="enquiry-form"
      noValidate
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit();
      }}
    >
      <h3>New Enquiry</h3>

      <label>
        Full Name *
        <input
          ref={nameInputRef}
          type="text"
          placeholder="Enter your full name"
          value={formData.name}
          onChange={(e) => onChange("name", e.target.value)}
        />
        {formErrors.name && <span className="form-error">{formErrors.name}</span>}
      </label>

      <div className="form-row">
        <label>
          Email Address *
          <input
            type="email"
            placeholder="name@gmail.com"
            value={formData.email}
            onChange={(e) => onChange("email", e.target.value)}
          />
          {formErrors.email && <span className="form-error">{formErrors.email}</span>}
        </label>

        <label className="phone-label">
          Mobile Number *
          <div className="phone-group">
            <select
              className="country-code-select"
              aria-label="Country code"
              value={formData.country_code}
              onChange={(e) => onChange("country_code", e.target.value)}
            >
              {COUNTRY_CODES.map((c) => (
                <option key={c.code} value={c.code}>
                  {c.name} ({c.code})
                </option>
              ))}
            </select>
            <input
              type="tel"
              inputMode="numeric"
              maxLength={15}
              value={formData.phone}
              onChange={(e) => onChange("phone", e.target.value.replace(/[^0-9]/g, ""))}
            />
          </div>
          {formErrors.phone && <span className="form-error">{formErrors.phone}</span>}
        </label>
      </div>

      <label>
        Service Required *
        <select value={formData.service} onChange={(e) => onChange("service", e.target.value)}>
          <option value="">Select a service...</option>
          {SERVICE_OPTIONS.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
        {formErrors.service && <span className="form-error">{formErrors.service}</span>}
      </label>

      <label>
        Product Name *
        <input
          type="text"
          value={formData.product_name}
          onChange={(e) => onChange("product_name", e.target.value)}
        />
        {formErrors.product_name && (
          <span className="form-error">{formErrors.product_name}</span>
        )}
      </label>

      <label>
        Company Name *
        <input
          type="text"
          value={formData.company_name}
          onChange={(e) => onChange("company_name", e.target.value)}
        />
        {formErrors.company_name && (
          <span className="form-error">{formErrors.company_name}</span>
        )}
      </label>

      <label>
        Purpose
        <textarea
          rows="2"
          value={formData.purpose}
          onChange={(e) => onChange("purpose", e.target.value)}
        />
      </label>

      <label>
        Scope of Testing
        <textarea
          rows="2"
          value={formData.scope}
          onChange={(e) => onChange("scope", e.target.value)}
        />
      </label>

      <label>
        Testing Standards
        <textarea
          rows="2"
          value={formData.testing_standards}
          onChange={(e) => onChange("testing_standards", e.target.value)}
        />
      </label>

      <label>
        Additional Details
        <textarea
          rows="2"
          placeholder="Anything else our team should know"
          value={formData.notes}
          onChange={(e) => onChange("notes", e.target.value)}
        />
      </label>



      <div className="form-actions">
        <button type="submit" className="form-submit" disabled={loading}>
          {loading ? "Submitting..." : "Submit Enquiry"}
        </button>
        <button type="button" className="form-cancel" onClick={onCancel}>
          Cancel
        </button>
      </div>
    </form>
  );
}

function ScheduleCallForm({ formData, formErrors, loading, onChange, onSubmit, onCancel, nameInputRef }) {
  return (
    <form
      className="enquiry-form"
      noValidate
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit();
      }}
    >
      <h3>Schedule a Callback</h3>

      <label>
        Name *
        <input
          ref={nameInputRef}
          type="text"
          placeholder="Enter your name"
          value={formData.name}
          onChange={(e) => onChange("name", e.target.value)}
        />
        {formErrors.name && <span className="form-error">{formErrors.name}</span>}
      </label>

      <label>
        Phone Number *
        <div className="phone-group">
          <select
            className="country-code-select"
            aria-label="Country code"
            value={formData.country_code}
            onChange={(e) => onChange("country_code", e.target.value)}
          >
            {COUNTRY_CODES.map((c) => (
              <option key={c.code} value={c.code}>
                {c.name} ({c.code})
              </option>
            ))}
          </select>
          <input
            type="tel"
            inputMode="numeric"
            maxLength={15}
            value={formData.phone}
            onChange={(e) => onChange("phone", e.target.value.replace(/[^0-9]/g, ""))}
            placeholder="10-digit mobile number"
          />
        </div>
        {formErrors.phone && <span className="form-error">{formErrors.phone}</span>}
      </label>

      <label>
        Email Address *
        <input
          type="email"
          placeholder="Enter your Gmail address"
          value={formData.email}
          onChange={(e) => onChange("email", e.target.value)}
        />
        {formErrors.email && <span className="form-error">{formErrors.email}</span>}
      </label>

      <label>
        Services *
        <select value={formData.service} onChange={(e) => onChange("service", e.target.value)}>
          <option value="">Select a service</option>
          {SERVICE_OPTIONS.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
        {formErrors.service && <span className="form-error">{formErrors.service}</span>}
      </label>

      <label>
        Purpose of the call
        <textarea
          rows="2"
          placeholder="Briefly describe the purpose of the call"
          value={formData.purpose}
          onChange={(e) => onChange("purpose", e.target.value)}
        />
      </label>



      <div className="form-actions">
        <button type="submit" className="form-submit" disabled={loading}>
          {loading ? "Submitting..." : "Submit"}
        </button>
        <button type="button" className="form-cancel" onClick={onCancel}>
          Cancel
        </button>
      </div>
    </form>
  );
}

function App() {
  const API_URL = "http://127.0.0.1:8000/chat/";

  const [sessionId, setSessionId] = useState(crypto.randomUUID());
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [currentStep, setCurrentStep] = useState("");
  const [lastAudio, setLastAudio] = useState(null);
  const [lastAlignment, setLastAlignment] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [activeCharIndex, setActiveCharIndex] = useState(-1);
  const audioRef = useRef(null);
  const animationRef = useRef(null);

  const [isListening, setIsListening] = useState(false);
  const recognitionRef = useRef(null);

  useEffect(() => {
    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      recognitionRef.current.lang = 'en-IN';

      recognitionRef.current.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInput((prev) => prev + (prev ? ' ' : '') + transcript);
      };

      recognitionRef.current.onerror = (event) => {
        console.error("Speech recognition error", event.error);
        setIsListening(false);
      };

      recognitionRef.current.onend = () => {
        setIsListening(false);
      };
    }
  }, []);


  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Hi! I am **Priya**, your AI Compliance Companion.\n\nWelcome to **ITC India**👋 \n\nBefore we begin, may I know your **NAME** and your **EMAIL ADDRESS**? It will help me personalize our conversation and assist you more effectively. 😊",
      time: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
    },
  ]);

  // Start with no option buttons shown; show query buttons only after onboarding
  const [options, setOptions] = useState([]);
  const [clickedOption, setClickedOption] = useState(null);

  useEffect(() => {
    if (!loading) setClickedOption(null);
  }, [loading]);

  // Enquiry form state
  const [showForm, setShowForm] = useState(false);
  const [showScheduleForm, setShowScheduleForm] = useState(false);
  const [onboardingDone, setOnboardingDone] = useState(false);
  const [widgetOpen, setWidgetOpen] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone: "",
    country_code: "+91",
    service: "",
    product_name: "",
    company_name: "",
    purpose: "",
    scope: "",
    testing_standards: "",
    notes: "",
    callback_time: "As soon as possible",
  });
  const [formErrors, setFormErrors] = useState({});
  const [scheduleFormData, setScheduleFormData] = useState({
    name: "",
    email: "",
    phone: "",
    country_code: "+91",
    service: "",
    purpose: "",
  });
  const [scheduleFormErrors, setScheduleFormErrors] = useState({});

  const chatEndRef = useRef(null);
  const chatContainerRef = useRef(null);
  const nameInputRef = useRef(null);
  const scheduleNameInputRef = useRef(null);
  const initDoneRef = useRef(false);
  const inputRef = useRef(null);

  useEffect(() => {
    if (widgetOpen && !loading && !showForm && !showScheduleForm) {
      const timer = setTimeout(() => {
        if (inputRef.current) {
          inputRef.current.focus();
        }
      }, 100);
      return () => clearTimeout(timer);
    }
  }, [widgetOpen, loading, showForm, showScheduleForm]);

  const checkAlignment = () => {
    if (!audioRef.current || audioRef.current.paused || !lastAlignment) {
      return;
    }

    const time = audioRef.current.currentTime;
    const starts = lastAlignment.character_start_times_seconds;
    const ends = lastAlignment.character_end_times_seconds;

    let foundIndex = -1;
    for (let i = starts.length - 1; i >= 0; i--) {
      if (time >= starts[i]) {
        foundIndex = i;
        break;
      }
    }

    setActiveCharIndex(foundIndex);
    animationRef.current = requestAnimationFrame(checkAlignment);
  };

  const toggleAudio = () => {
    if (!lastAudio) return;

    if (isPlaying && audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
      setIsPlaying(false);
      setActiveCharIndex(-1);
      if (animationRef.current) cancelAnimationFrame(animationRef.current);
    } else {
      if (audioRef.current) {
        audioRef.current.pause();
      }
      const newAudio = new Audio("data:audio/mp3;base64," + lastAudio);
      audioRef.current = newAudio;
      newAudio.onended = () => {
        setIsPlaying(false);
        setActiveCharIndex(-1);
        if (animationRef.current) cancelAnimationFrame(animationRef.current);
      };
      newAudio.play().then(() => {
        setIsPlaying(true);
        animationRef.current = requestAnimationFrame(checkAlignment);
      }).catch(e => console.error("Audio playback failed:", e));
    }
  };
  const lastOptionsRef = useRef([]);
  const lastSubmittedRef = useRef(null);
  const editModeRef = useRef(false);
  const onboardingRef = useRef({ name: "", email: "" });

  // Initialise backend conversation state on mount (so the first click works)
  useEffect(() => {
    if (initDoneRef.current) return;
    initDoneRef.current = true;

    const init = async () => {
      try {
        // If we have saved onboarding (name+email), bootstrap the backend with it so
        // the server returns the post-onboarding options (services). Otherwise keep
        // the UI minimal (only new/existing) until the user completes onboarding.
        const saved = window.localStorage.getItem("itc_onboarding");
        const onboarding = saved ? JSON.parse(saved) : null;
        if (onboarding && onboarding.name && onboarding.email) {
          onboardingRef.current = { ...onboardingRef.current, ...onboarding };
          setOnboardingDone(true);
        }

        const initBody = onboarding && onboarding.name && onboarding.email
          ? { session_id: sessionId, message: `My name is ${onboarding.name} and my email is ${onboarding.email}` }
          : { session_id: sessionId, message: "" };

        const response = await fetch(API_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(initBody),
        });
        if (!response.ok) return;
        const data = await response.json();
        if (data.audio) {
          setLastAudio(data.audio);
          setLastAlignment(data.alignment || null);
          setIsPlaying(false);
          setActiveCharIndex(-1);
        }
        setCurrentStep(data.step || "");
        if (data.intent === "GREETING" && data.answer) {
          setMessages([
            {
              role: "assistant",
              content: data.answer,
              time: new Date().toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
              }),
            },
          ]);

          // If we already had onboarding persisted, allow server options (services).
          if (onboarding && onboarding.name && onboarding.email) {
            if (data.options?.length) {
              setOptions(data.options);
              lastOptionsRef.current = data.options;
            }
          } else {
            // Keep initial UI minimal: no buttons shown until onboarding completes
            setOptions([]);
          }

          if (data.onboarding) {
            onboardingRef.current = { ...onboardingRef.current, ...data.onboarding };
            // persist onboarding when server provides it
            try {
              window.localStorage.setItem("itc_onboarding", JSON.stringify(onboardingRef.current));
            } catch (e) { }
            setOnboardingDone(true);
          }
        }
      } catch {
        // backend not running yet - keep default options
      }
    };
    init();
  }, [sessionId]);

  useEffect(() => {
    if (showForm) return;

    const container = chatContainerRef.current;
    if (container) {
      const messageElements = container.querySelectorAll(".message");
      const lastMessage = messageElements[messageElements.length - 1];
      if (lastMessage) {
        // If it is the assistant, align its top to the view so the user can start reading it.
        // If it fits on screen, the browser naturally clamps to the bottom.
        if (lastMessage.classList.contains("assistant")) {
          lastMessage.scrollIntoView({ behavior: "smooth", block: "start" });
        } else {
          chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
        }
        return;
      }
    }
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, options, showForm]);

  // When the enquiry form opens, bring its top into view (instant scroll so
  // clicks on the fields land correctly, especially on small screens).
  useEffect(() => {
    if (showForm) {
      requestAnimationFrame(() => {
        nameInputRef.current?.focus();
      });
    }
  }, [showForm]);

  const addMessage = (role, content, service_table = null, footer = null) => {
    setMessages((prev) => [
      ...prev,
      {
        role,
        content,
        service_table,
        footer,
        time: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      },
    ]);
  };

  const toggleListening = () => {
    if (!recognitionRef.current) {
      addMessage("assistant", "Sorry, your browser does not support speech recognition. Please type your message instead.");
      return;
    }
    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      recognitionRef.current.start();
      setIsListening(true);
    }
  };

  const submitMessage = async (question) => {
    if (!question.trim()) return;

    const normalized = question.trim().toLowerCase();
    if (
      normalized.includes("new enquiry") ||
      normalized.includes("new query") ||
      normalized.includes("new enquir") ||
      normalized.includes("new customer")
    ) {
      openEnquiryForm(question);
      return;
    }

    if (
      normalized.includes("schedule a call") ||
      normalized.includes("arrange a call") ||
      normalized.includes("arange a call") ||
      normalized.includes("request a callback") ||
      (normalized.includes("schedule") && normalized.includes("call")) ||
      normalized === "callback"
    ) {
      openScheduleForm(question);
      return;
    }

    addMessage("user", question);
    setOptions([]);
    setShowForm(false);
    setLoading(true);

    try {
      await new Promise((resolve) => setTimeout(resolve, 800 + Math.random() * 400));
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          session_id: sessionId,
          message: question,
        }),
      });

      if (!response.ok) {
        throw new Error("Backend Error");
      }

      const data = await response.json();
      if (data.audio) {
        setLastAudio(data.audio);
        setLastAlignment(data.alignment || null);
        setIsPlaying(false);
        setActiveCharIndex(-1);
      }
      setCurrentStep(data.step || "");

      if (data.onboarding) {
        onboardingRef.current = { ...onboardingRef.current, ...data.onboarding };
        try {
          window.localStorage.setItem("itc_onboarding", JSON.stringify(onboardingRef.current));
        } catch (e) { }
      }
      if (data.onboarding) setOnboardingDone(true);

      const isEnquiryFormStart =
        data.step === "name" && data.intent === "NEW_ENQUIRY";

      addMessage(
        "assistant",
        isEnquiryFormStart
          ? "Great, happy to help!\n\nPlease fill in your details below and our team will contact you."
          : data.answer,
        data.service_table,
        data.footer
      );

      if (isEnquiryFormStart) {
        setFormData({
          name: onboardingRef.current.name || "",
          email: onboardingRef.current.email || "",
          phone: "",
          country_code: "+91",
          service: "",
          product_name: "",
          company_name: "",
          purpose: "",
          scope: "",
          testing_standards: "",
          notes: "",
          callback_time: "As soon as possible",
        });
        setShowForm(true);
        setOptions([]);
      } else {
        setOptions(data.options ?? []);
        if (data.options?.length) lastOptionsRef.current = data.options;
      }
    } catch {
      addMessage(
        "assistant",
        "❌ Unable to connect to backend. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleSend = async () => {
    if (!input.trim()) return;
    const question = input;
    setInput("");
    await submitMessage(question);
  };

  const openEnquiryForm = (sourceMessage) => {
    editModeRef.current = false;
    if (sourceMessage) {
      addMessage("user", sourceMessage);
    }
    addMessage(
      "assistant",
      "Great, happy to help!\n\nPlease fill in your details below and our team will contact you."
    );
    setFormData({
      name: onboardingRef.current.name || "",
      email: onboardingRef.current.email || "",
      phone: "",
      country_code: "+91",
      service: "",
      product_name: "",
      company_name: "",
      purpose: "",
      scope: "",
      testing_standards: "",
      notes: "",
      callback_time: "As soon as possible",
    });
    setOptions([]);
    setFormErrors({});
    setShowForm(true);
  };

  const openEditForm = () => {
    editModeRef.current = true;
    const prev = lastSubmittedRef.current;
    if (prev) {
      setFormData({ ...prev });
    }
    setFormErrors({});
    setOptions([]);
    setShowForm(true);
  };

  const openScheduleForm = (sourceMessage) => {
    editModeRef.current = false;
    if (sourceMessage) {
      addMessage("user", sourceMessage);
    }
    const saved = lastSubmittedRef.current ?? {};
    const savedPhone = saved.phone || "";

    setScheduleFormData({
      name: saved.name || onboardingRef.current.name || "",
      email: saved.email || onboardingRef.current.email || "",
      phone: savedPhone,
      country_code: saved.country_code || "+91",
      service: saved.service || "",
      purpose: "",
    });
    addMessage("assistant", "Please complete the callback request below so our team can contact you.");
    setScheduleFormErrors({});
    setOptions([]);
    setShowScheduleForm(true);
  };

  const closeEnquiryForm = () => {
    setShowForm(false);
    setFormErrors({});
    setOptions(lastOptionsRef.current ?? []);
    editModeRef.current = false;
  };

  const closeScheduleForm = () => {
    setShowScheduleForm(false);
    setScheduleFormErrors({});
    setOptions(lastOptionsRef.current ?? []);
  };

  const handleOptionClick = async (option) => {
    setClickedOption(option);
    const normalized = option.toLowerCase();

    if (normalized.includes("schedule") || normalized.includes("callback")) {
      openScheduleForm(option);
      return;
    }

    if (
      normalized.includes("new enquiry") ||
      normalized.includes("new query") ||
      normalized.includes("new customer")
    ) {
      openEnquiryForm(option);
      return;
    }

    if (normalized.includes("edit my details")) {
      openEditForm();
      return;
    }

    await submitMessage(option);
  };

  const handleSoftRestart = () => {
    const name = onboardingRef.current.name;
    const email = onboardingRef.current.email;

    if (!name || !email) {
      initDoneRef.current = false;
      setSessionId(crypto.randomUUID());
      setMessages([]);
      setOptions([]);
      setShowForm(false);
      setFormErrors({});
      try { window.localStorage.removeItem("itc_onboarding"); } catch (e) { }
      setOnboardingDone(false);
      return;
    }

    const newSessionId = crypto.randomUUID();
    setSessionId(newSessionId);
    setCurrentStep("");

    setMessages([
      {
        role: "assistant",
        content: `Welcome, **${name}**! 👋\n\n**ITC India** is your trusted partner for NABL-accredited testing and certification. How can I assist you today?\n\nYou may select one of the options below to get started, or type your question in the message box.`,
        time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      }
    ]);
    setOptions([
      "I have a new query",
      "I have an existing query",
      "Electrical Safety Testing",
      "EMC/EMI Testing",
      "Electro-Medical Equipment",
      "Photometry (LM-79/LM-80)",
      "Environmental / IP Testing",
      "Calibration Services",
      "Packaging Testing",
      "Software Testing",
      "Information Security"
    ]);
    setShowForm(false);
    setFormErrors({});

    fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id: newSessionId,
        message: `My name is ${name} and my email is ${email}`
      }),
    }).catch(() => { });
  };

  const handleHardRestart = () => {
    initDoneRef.current = false;
    setSessionId(crypto.randomUUID());
    setCurrentStep("");
    setMessages([
      {
        role: "assistant",
        content:
          "Hi! I am **Priya**, your AI Compliance Companion.\n\nWelcome to **ITC India**👋 \n\nBefore we begin, may I know your **NAME** and your **EMAIL ADDRESS**? It will help me personalize our conversation and assist you more effectively. 😊",
        time: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      }
    ]);
    setOptions([]);
    setShowForm(false);
    setFormErrors({});
    onboardingRef.current = { name: "", email: "" };
    try { window.localStorage.removeItem("itc_onboarding"); } catch (e) { }
    setOnboardingDone(false);
    setWidgetOpen(false);
  };

  // ========== ENQUIRY FORM ==========

  const validateForm = () => {
    const errors = {};

    if (!formData.name.trim()) {
      errors.name = "Please enter your full name.";
    } else if (formData.name.trim().length < 2) {
      errors.name = "Name must be at least 2 characters.";
    }

    if (!EMAIL_REGEX.test(formData.email.trim())) {
      errors.email = "Please enter a valid email address (e.g., name@gmail.com).";
    } else {
      const local = formData.email.trim().split("@")[0];
      if (!/[a-zA-Z]/.test(local)) {
        errors.email = "Please enter a valid email address (e.g., name@gmail.com).";
      }
    }

    const country =
      COUNTRY_CODES.find((c) => c.code === formData.country_code) ?? null;
    const minDigits = country?.minDigits ?? 7;
    const maxDigits = country?.maxDigits ?? 15;
    const localDigits = formData.phone.replace(/\D/g, "");
    const fullPhone = `${formData.country_code}${localDigits}`;
    const lengthOk =
      localDigits.length >= minDigits && localDigits.length <= maxDigits;

    if (!PHONE_REGEX.test(fullPhone) || !lengthOk) {
      errors.phone =
        minDigits === maxDigits
          ? `Please enter a valid ${minDigits}-digit mobile number (without the country code).`
          : `Please enter a valid ${minDigits}-${maxDigits} digit mobile number (without the country code).`;
    }

    if (!formData.service) {
      errors.service = "Please select a service.";
    }

    if (!formData.product_name.trim()) {
      errors.product_name = "Please enter the product name.";
    } else if (formData.product_name.trim().length < 2) {
      errors.product_name = "Product name must be at least 2 characters.";
    }

    if (!formData.company_name.trim()) {
      errors.company_name = "Please enter the company name.";
    } else if (formData.company_name.trim().length < 2) {
      errors.company_name = "Company name must be at least 2 characters.";
    }

    return errors;
  };

  const validateScheduleForm = () => {
    const errors = {};

    if (!scheduleFormData.name.trim()) {
      errors.name = "Please enter your name.";
    }

    const fullPhone = `${scheduleFormData.country_code}${scheduleFormData.phone.replace(/\D/g, "")}`;
    const country = COUNTRY_CODES.find((c) => c.code === scheduleFormData.country_code) ?? null;
    const minDigits = country?.minDigits ?? 7;
    const maxDigits = country?.maxDigits ?? 15;
    const localDigits = scheduleFormData.phone.replace(/\D/g, "");
    const lengthOk = localDigits.length >= minDigits && localDigits.length <= maxDigits;
    if (!PHONE_REGEX.test(fullPhone) || !lengthOk) {
      errors.phone =
        minDigits === maxDigits
          ? `Please enter a valid ${minDigits}-digit mobile number (without the country code).`
          : `Please enter a valid ${minDigits}-${maxDigits} digit mobile number (without the country code).`;
    }

    if (!EMAIL_REGEX.test(scheduleFormData.email.trim())) {
      errors.email = "Please enter a valid email address (e.g., name@gmail.com).";
    }

    if (!scheduleFormData.service) {
      errors.service = "Please select a service.";
    }

    return errors;
  };

  const handleScheduleSubmit = async () => {
    const errors = validateScheduleForm();
    setScheduleFormErrors(errors);
    if (Object.keys(errors).length > 0) return;

    const fullPhone = `${scheduleFormData.country_code}${scheduleFormData.phone.replace(/\D/g, "")}`;
    addMessage(
      "user",
      `**Schedule Callback Request**\n• **Name**: ${scheduleFormData.name.trim()}\n• **Email**: ${scheduleFormData.email.trim()}\n• **Phone**: ${fullPhone}\n• **Service**: ${scheduleFormData.service}\n• **Purpose**: ${scheduleFormData.purpose.trim() || "N/A"}`
    );
    setShowScheduleForm(false);
    setLoading(true);

    try {
      await new Promise((resolve) => setTimeout(resolve, 1000));
      
      const saved = lastSubmittedRef.current ?? {};
      
      const response = await fetch(`${API_URL}enquiry/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: sessionId,
          name: scheduleFormData.name.trim(),
          email: scheduleFormData.email.trim(),
          phone: fullPhone,
          service: scheduleFormData.service,
          product_name: saved.product_name ? saved.product_name.trim() : scheduleFormData.service,
          company_name: saved.company_name ? saved.company_name.trim() : "N/A",
          purpose: scheduleFormData.purpose.trim() || (saved.purpose ? saved.purpose.trim() : ""),
          scope: saved.scope ? saved.scope.trim() : "",
          notes: `Schedule a callback`,
        }),
      });

      if (!response.ok) {
        throw new Error("Backend Error");
      }

      const data = await response.json();
      if (data.audio) {
        setLastAudio(data.audio);
        setLastAlignment(data.alignment || null);
        setIsPlaying(false);
        setActiveCharIndex(-1);
      }
      lastSubmittedRef.current = { ...scheduleFormData };
      addMessage("assistant", data.answer);
      setOptions(data.options ?? []);
      editModeRef.current = false;
    } catch {
      addMessage(
        "assistant",
        "❌ Unable to submit your callback request. Please try again."
      );
      setOptions([]);
    } finally {
      setLoading(false);
    }
  };

  const handleEnquirySubmit = async () => {
    const errors = validateForm();
    setFormErrors(errors);
    if (Object.keys(errors).length > 0) return;

    const fullPhone = `${formData.country_code}${formData.phone.replace(/\D/g, "")}`;

    const summary =
      `**New Enquiry Details**\n` +
      `• **Name**: ${formData.name.trim()}\n` +
      `• **Email**: ${formData.email.trim()}\n` +
      `• **Phone**: ${fullPhone}\n` +
      `• **Service**: ${formData.service}\n` +
      `• **Product**: ${formData.product_name.trim()}\n` +
      `• **Company Name**: ${formData.company_name.trim() || "N/A"}\n` +
      `• **Purpose**: ${formData.purpose.trim() || "N/A"}\n` +
      `• **Scope of Testing**: ${formData.scope.trim() || "N/A"}\n` +
      `• **Testing Standards**: ${formData.testing_standards.trim() || "N/A"}\n` +
      `• **Additional Details**: ${formData.notes.trim() || "N/A"}`;

    addMessage("user", summary);
    setShowForm(false);
    setLoading(true);

    try {
      await new Promise((resolve) => setTimeout(resolve, 1000));
      const response = await fetch(`${API_URL}enquiry/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: sessionId,
          name: formData.name.trim(),
          email: formData.email.trim(),
          phone: fullPhone,
          service: formData.service,
          product_name: formData.product_name.trim(),
          company_name: formData.company_name.trim(),
          purpose: formData.purpose.trim(),
          scope: formData.scope.trim(),
          notes: formData.testing_standards?.trim()
            ? `Testing Standards: ${formData.testing_standards.trim()}\n\n${formData.notes.trim()}`
            : formData.notes.trim(),
        }),
      });

      if (!response.ok) {
        throw new Error("Backend Error");
      }

      const data = await response.json();
      if (data.audio) {
        setLastAudio(data.audio);
        setLastAlignment(data.alignment || null);
        setIsPlaying(false);
        setActiveCharIndex(-1);
      }
      lastSubmittedRef.current = { ...formData };
      addMessage("assistant", data.answer);
      // Persist onboarding once the form is submitted successfully
      try {
        onboardingRef.current = { name: formData.name.trim(), email: formData.email.trim() };
        window.localStorage.setItem("itc_onboarding", JSON.stringify(onboardingRef.current));
      } catch (e) { }
      setOnboardingDone(true);
      const serverOptions = data.options ?? [];
      lastOptionsRef.current = serverOptions;

      setOptions(serverOptions);
      editModeRef.current = false;
      setFormData({
        name: "",
        email: "",
        phone: "",
        country_code: "+91",
        service: "",
        product_name: "",
        company_name: "",
        purpose: "",
        scope: "",
        testing_standards: "",
        notes: "",
        callback_time: "As soon as possible",
      });
    } catch {
      addMessage(
        "assistant",
        "❌ Unable to submit your enquiry. Please try again."
      );
      setOptions([]);
    } finally {
      setLoading(false);
    }
  };

  const getPlaceholder = () => {
    if (showForm) return "Please complete the enquiry form above...";
    if (!currentStep) return "Type your message...";
    if (currentStep.includes("name")) return "Enter your full name";
    if (currentStep.includes("email") || currentStep === "lookup_by_email") return "Enter your email address";
    if (currentStep.includes("phone")) return "Enter your 10-digit phone number";
    if (["description", "notes", "purpose"].includes(currentStep)) return "Describe your issue";
    if (currentStep === "gcontact") {
      if (!onboardingRef.current.name) return "Enter your full name";
      if (!onboardingRef.current.email) return "Enter your email address";
    }
    return "Type your message...";
  };

  return widgetOpen ? (
    <div className={`app ${isExpanded ? "expanded" : ""}`}>
      <header className="header">
        <div className="logo">
          <img src={avatarImg} alt="Priya" className="header-avatar-img" />
        </div>
        <div className="header-text">
          <h2>PRIYA</h2>
          <p>Your ITC India Assistant</p>
        </div>
        <div className="header-actions">
          <span className="status-dot" />
          <button className="header-btn" title="Restart" onClick={handleSoftRestart}>↻</button>
          <button
            className="header-btn"
            title={isExpanded ? "Collapse" : "Expand"}
            onClick={() => setIsExpanded(!isExpanded)}
          >
            {isExpanded ? "◱" : "⛶"}
          </button>
          <button
            type="button"
            className="header-btn"
            onClick={handleHardRestart}
            aria-label="Minimize chat"
            title="Minimize"
          >
            ×
          </button>
        </div>
      </header>

      <main className="chat-container" ref={chatContainerRef}>
        <div className="messages">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.role}`}>
              <div className="avatar">
                {msg.role === "assistant" ? <img src={avatarImg} alt="Priya" className="message-avatar-img" /> : (
                  <svg className="user-icon-svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 12C14.21 12 16 10.21 16 8C16 5.79 14.21 4 12 4C9.79 4 8 5.79 8 8C8 10.21 9.79 12 12 12ZM12 14C9.33 14 4 15.34 4 18V20H20V18C20 15.34 14.67 14 12 14Z" />
                  </svg>
                )}
              </div>
              <div className="bubble">
                <MessageContent
                  content={msg.content}
                  isHighlighted={isPlaying && index === messages.length - 1}
                  activeCharIndex={activeCharIndex}
                />
                {msg.service_table && (
                  <ServiceTable tableData={msg.service_table} />
                )}
                {msg.footer && (
                  <div style={{ marginTop: '12px' }}>
                    <MessageContent content={msg.footer} />
                  </div>
                )}
              </div>
            </div>
          ))}

          {showForm && (
            <div className="enquiry-overlay">
              <div className="enquiry-panel">
                <div className="enquiry-header">
                  <div>
                    <h3>New Enquiry</h3>
                    <p>Please fill in your details and submit the form below.</p>
                  </div>
                  <button
                    type="button"
                    className="enquiry-close"
                    onClick={closeEnquiryForm}
                  >
                    ×
                  </button>
                </div>
                <EnquiryForm
                  formData={formData}
                  formErrors={formErrors}
                  loading={loading}
                  nameInputRef={nameInputRef}
                  onChange={(field, value) => {
                    setFormData((prev) => ({ ...prev, [field]: value }));
                    setFormErrors((prev) => ({ ...prev, [field]: undefined }));
                  }}
                  onSubmit={handleEnquirySubmit}
                  onCancel={closeEnquiryForm}
                />
              </div>
            </div>
          )}

          {showScheduleForm && (
            <div className="enquiry-overlay">
              <div className="enquiry-panel">
                <div className="enquiry-header">
                  <div>
                    <h3>Schedule a Call</h3>
                    <p>Auto-filled from your enquiry details. Update if needed and submit.</p>
                  </div>
                  <button
                    type="button"
                    className="enquiry-close"
                    onClick={closeScheduleForm}
                  >
                    ×
                  </button>
                </div>
                <ScheduleCallForm
                  formData={scheduleFormData}
                  formErrors={scheduleFormErrors}
                  loading={loading}
                  nameInputRef={scheduleNameInputRef}
                  onChange={(field, value) => {
                    setScheduleFormData((prev) => ({ ...prev, [field]: value }));
                    setScheduleFormErrors((prev) => ({ ...prev, [field]: undefined }));
                  }}
                  onSubmit={handleScheduleSubmit}
                  onCancel={closeScheduleForm}
                />
              </div>
            </div>
          )}

          {loading && (
            <div className="message assistant">
              <div className="avatar">
                <img src={avatarImg} alt="Priya" className="message-avatar-img" />
              </div>
              <div className="bubble typing-bubble">
                <span className="dot" />
                <span className="dot" />
                <span className="dot" />
              </div>
            </div>
          )}

          <div ref={chatEndRef}></div>

          {(() => {
            // Only show option chips after onboarding is complete or while the form is open.
            if (!onboardingDone && !showForm) return null;
            if (options.length === 0) return null;
            const topPrimaryOptions = options.filter((opt) => {
              const lower = opt.toLowerCase();
              return (
                opt.includes("✏️") ||
                opt.includes("📞") ||
                lower === "edit my details" ||
                lower === "schedule a call"
              );
            });
            const bottomPrimaryOptions = options.filter((opt) => {
              const lower = opt.toLowerCase();
              return (
                lower.includes("new query") ||
                lower.includes("new enquiry") ||
                lower.includes("existing query") ||
                lower.includes("old query") ||
                lower === "new customer" ||
                lower === "existing customer"
              );
            });
            const callbackOptions = options.filter((opt) => {
              const lower = opt.toLowerCase();
              return lower === "request callback" || lower === "request a callback";
            });
            const secondaryOptions = options.filter(
              (opt) =>
                !topPrimaryOptions.includes(opt) &&
                !bottomPrimaryOptions.includes(opt) &&
                !callbackOptions.includes(opt)
            );

            return (
              <div className="workflow-options">
                {topPrimaryOptions.length > 0 && (
                  <div className="chips primary-chips">
                    {topPrimaryOptions.map((option, index) => (
                      <button
                        key={`top-pri-${index}`}
                        className="chip chip-primary"
                        onClick={() => handleOptionClick(option)}
                        disabled={loading}
                      >
                        {option}
                      </button>
                    ))}
                  </div>
                )}
                {(secondaryOptions.length > 0 || callbackOptions.length > 0) && (
                  <div className="chips secondary-chips">
                    {secondaryOptions.map((option, index) => (
                      <button
                        key={`sec-${index}`}
                        className="chip chip-secondary"
                        onClick={() => handleOptionClick(option)}
                        disabled={loading}
                      >
                        {option}
                      </button>
                    ))}
                    {callbackOptions.map((option, index) => (
                      <button
                        key={`callback-${index}`}
                        className="chip chip-callback"
                        onClick={() => handleOptionClick(option)}
                        disabled={loading}
                      >
                        {option}
                      </button>
                    ))}
                  </div>
                )}
                {bottomPrimaryOptions.length > 0 && (
                  <div className="chips primary-chips">
                    {bottomPrimaryOptions.map((option, index) => (
                      <button
                        key={`bot-pri-${index}`}
                        className="chip chip-primary"
                        onClick={() => handleOptionClick(option)}
                        disabled={loading}
                      >
                        {option}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            );
          })()}
        </div>
      </main>

      <footer className="footer-container">
        {lastAudio && (
          <div className="audio-replay-container">
            <button
              className="replay-audio-btn"
              onClick={toggleAudio}
              title={isPlaying ? "Stop audio" : "Listen to last response"}
              aria-label="Replay audio"
            >
              {isPlaying ? (
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                  <rect x="6" y="6" width="12" height="12" rx="2" />
                </svg>
              ) : (
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M11 5L6 9H2V15H6L11 19V5Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                  <path d="M15.54 8.46C16.4774 9.39764 17.004 10.6692 17.004 11.995C17.004 13.3208 16.4774 14.5924 15.54 15.53" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                  <path d="M19.07 4.92999C20.9447 6.80527 21.9979 9.34835 21.9979 12C21.9979 14.6516 20.9447 17.1947 19.07 19.07" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              )}
            </button>
          </div>
        )}
        <div className="input-area">
          <input
            ref={inputRef}
            type="text"
            placeholder={getPlaceholder()}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") handleSend();
            }}
            disabled={loading || showForm}
          />
          <button
            className={`mic-btn ${isListening ? 'listening' : ''}`}
            onClick={toggleListening}
            disabled={loading || showForm}
            title={isListening ? "Stop listening" : "Start voice input"}
            aria-label="Voice input"
          >
            {isListening ? (
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                <rect x="6" y="6" width="12" height="12" rx="2" />
              </svg>
            ) : (
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z"></path>
                <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
                <line x1="12" y1="19" x2="12" y2="23"></line>
                <line x1="8" y1="23" x2="16" y2="23"></line>
              </svg>
            )}
          </button>
          <button className="send-btn" onClick={handleSend} disabled={loading || showForm}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M22 2L11 13M22 2L15 22L11 13M11 13L2 9L22 2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </button>
        </div>
        <div className="powered-by">
          Powered by <a href="https://evokeaisolutions.com/" target="_blank" rel="noopener noreferrer">Evoke AI</a>
        </div>
      </footer>
    </div>
  ) : (
    <div
      className="widget-trigger"
      onClick={() => setWidgetOpen(true)}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") setWidgetOpen(true);
      }}
      role="button"
      tabIndex={0}
      aria-label="Open chat"
    >
      <span className="widget-label">Hi! 👋 Need help? Chat with us</span>
      <div className="widget-avatar">
        <img src={avatarImg} alt="Priya" className="widget-avatar-img" />
        <span className="widget-dot" />
      </div>
    </div>
  );
}

export default App;
