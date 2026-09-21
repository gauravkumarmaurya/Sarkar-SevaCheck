import React, { useEffect, useMemo, useRef, useState } from "react";
import L from "leaflet";
import { api } from "./api";

const DEMO_ADMIN = "9999999999";
const DEMO_CITIZEN = "9876543210";

const DISTRICTS = [
  ["Dehradun", 30.3165, 78.0322], ["Haridwar", 29.9457, 78.1642],
  ["Nainital", 29.3919, 79.4542], ["Udham Singh Nagar", 28.9800, 79.5154],
  ["Almora", 29.5971, 79.6591], ["Pauri Garhwal", 30.1483, 78.7783],
  ["Tehri Garhwal", 30.3786, 78.4800], ["Uttarkashi", 30.7268, 78.4354],
  ["Chamoli", 30.4057, 79.2150], ["Rudraprayag", 30.2843, 78.9811],
  ["Bageshwar", 29.8376, 79.7709], ["Champawat", 29.3369, 80.0910],
  ["Pithoragarh", 29.5829, 80.2182]
];

const T = {
  en: {
    dashboard: "Dashboard", ocr: "Receipt OCR", map: "Service Map", reports: "My Reports", admin: "Admin",
    login: "Login", register: "Register", logout: "Logout", hindi: "हिंदी", english: "English",
    before: "BEFORE YOU PAY", subtitle: "Government fee transparency",
    source: "Use the source evidence and verification badge — not an unsupported number — to decide what to ask for.",
    total: "Total services", official: "Official verified", demo: "Demo/Test data", search: "Search services...",
    gov: "Government fee", serviceCharge: "Authorized service charge", other: "Other allowed charge", payable: "Documented payable",
    apply: "Apply officially", feeSource: "Fee source", demoWarning: "Synthetic demo amount — NOT an official government fee.",
    verified: "OFFICIAL DATA VERIFIED", demoBadge: "DEMO / TEST DATA", verify: "VERIFY SOURCE", awaiting: "Awaiting verification",
    processing: "Processing", documents: "Documents", know: "Know", applyStep: "Apply", pay: "Pay", verifyStep: "Verify", report: "Report",
    flow: "ONE SIMPLE FLOW", flowText: ["See the documented fee and official source.", "Open the government portal.", "Ask for a receipt/payment evidence.", "Compare payment with documented data.", "Send evidence to the proper channel."],
    accuracy: "Important accuracy rule", accuracyText: "SevaCheck does not declare that a person, CSC or office is corrupt. Official fee records must be verified from current government sources. Demo amounts are synthetic hackathon test values.",
    receiptTitle: "Receipt OCR + Payment Check", receiptHint: "Upload one of the synthetic demo receipts to test OCR and comparison.",
    chooseService: "Choose service", chooseFile: "Choose receipt image", runOCR: "Scan receipt", result: "Check result",
    extracted: "OCR extracted amount", documented: "Documented/demo amount", noFile: "Please select a receipt image.",
    noService: "Please select a service.", demoCheck: "This comparison uses synthetic hackathon data and is not an official fee determination.",
    compareAbove: "Paid amount documented amount se zyada hai.", compareWithin: "Payment is within the documented/demo amount", comparisonUnavailable: "Fee verification required before comparison.",
    loginHint: "Demo citizen: 9876543210 · Demo admin: 9999999999", mobile: "Mobile number", name: "Name", continue: "Continue",
    noReports: "No reports yet.", reportsTitle: "My submitted checks", paid: "Paid", status: "Status", submitReport: "Submit report",
    note: "Citizen note", reportSent: "Report submitted successfully.", loginRequired: "Login required for reports.",
    adminTitle: "Admin control panel", create: "Create service", save: "Save", edit: "Edit", delete: "Delete", cancel: "Cancel",
    adminOnly: "Admin access only.", confirmDelete: "Delete this service?", saved: "Saved successfully.", added: "Service added.", deleted: "Service deleted.",
    totalReports: "Total reports", excessOfficial: "Above official total", excessDemo: "Above demo total", needsVerify: "Needs fee verification",
    demoMap: "District-level demo map", mapNote: "Markers are demonstration points. Service values are shown according to their verification badge.",
    servicesAvailable: "services shown", loading: "Loading...", apiError: "Could not load data. Check that the backend is running.",
    noResults: "No matching services."
  },
  hi: {
    dashboard: "Dashboard", ocr: "Receipt OCR", map: "Service Map", reports: "My Reports", admin: "Admin",
    login: "Login", register: "Register", logout: "Logout", hindi: "हिंदी", english: "English",
    before: "BEFORE YOU PAY", subtitle: "सरकारी शुल्क पारदर्शिता",
    source: "किसी unsupported number के बजाय source evidence और verification badge देखकर शुल्क समझें।",
    total: "Total services", official: "Official verified", demo: "Demo/Test data", search: "Search services...",
    gov: "Government fee", serviceCharge: "Authorized service charge", other: "Other allowed charge", payable: "Documented payable",
    apply: "आधिकारिक रूप से आवेदन करें", feeSource: "Fee source", demoWarning: "Synthetic demo amount — यह official government fee नहीं है।",
    verified: "OFFICIAL DATA VERIFIED", demoBadge: "DEMO / TEST DATA", verify: "VERIFY SOURCE", awaiting: "Verification बाकी है",
    processing: "Processing", documents: "Documents", know: "जानें", applyStep: "Apply", pay: "Pay", verifyStep: "Verify", report: "Report",
    flow: "ONE SIMPLE FLOW", flowText: ["दस्तावेज़ित शुल्क और source देखें।", "Government portal खोलें।", "Receipt/payment evidence लें।", "Payment को documented data से compare करें।", "Evidence उचित channel पर भेजें।"],
    accuracy: "Important accuracy rule", accuracyText: "SevaCheck किसी व्यक्ति, CSC या office को corrupt घोषित नहीं करता। Official fee records को current government sources से verify करना जरूरी है। Demo amounts synthetic hackathon test values हैं।",
    receiptTitle: "Receipt OCR + Payment Check", receiptHint: "OCR और comparison test करने के लिए synthetic demo receipt upload करें।",
    chooseService: "Service चुनें", chooseFile: "Receipt image चुनें", runOCR: "Scan receipt", result: "Check result",
    extracted: "OCR extracted amount", documented: "Documented/demo amount", noFile: "पहले receipt image चुनें।",
    noService: "पहले service चुनें।", demoCheck: "यह comparison synthetic hackathon data पर आधारित है और official fee determination नहीं है।",
    compareAbove: "Paid amount documented amount se zyada hai.", compareWithin: "Payment documented/demo amount के अंदर है", comparisonUnavailable: "Fee verification required before comparison.",
    loginHint: "Demo citizen: 9876543210 · Demo admin: 9999999999", mobile: "Mobile number", name: "Name", continue: "Continue",
    noReports: "अभी कोई report नहीं है।", reportsTitle: "मेरी submitted checks", paid: "Paid", status: "Status", submitReport: "Report submit करें",
    note: "Citizen note", reportSent: "Report successfully submit हो गई।", loginRequired: "Reports देखने के लिए login करें।",
    adminTitle: "Admin control panel", create: "Create service", save: "Save", edit: "Edit", delete: "Delete", cancel: "Cancel",
    adminOnly: "Admin access only.", confirmDelete: "क्या इस service को delete करना है?", saved: "Saved successfully.", added: "Service added.", deleted: "Service deleted.",
    totalReports: "Total reports", excessOfficial: "Above official total", excessDemo: "Above demo total", needsVerify: "Needs fee verification",
    demoMap: "District-level demo map", mapNote: "Markers demonstration points हैं। Service values badge के अनुसार दिखाई जाती हैं।",
    servicesAvailable: "services shown", loading: "Loading...", apiError: "Data load नहीं हुआ। Backend चल रहा है या नहीं देखें।",
    noResults: "Matching service नहीं मिली।"
  }
};

function isOfficial(service) { return ["VERIFIED", "VERIFIED_OFFICIAL"].includes(service?.fee_status); }
function isDemo(service) { return service?.fee_status === "DEMO_DATA"; }
function hasFee(service) { return isOfficial(service) || isDemo(service); }
function totalFee(service) {
  if (!hasFee(service)) return null;
  return Number(service.government_fee || 0) + Number(service.authorized_service_charge || 0) + Number(service.other_allowed_charge || 0);
}
function money(value) { return `₹${Number(value || 0).toFixed(2)}`; }

function Header({ lang, setLang, user, onLogout, page, setPage }) {
  const t = T[lang];
  return <header className="topbar">
    <div className="brand" onClick={() => setPage("dashboard")}>
      <div className="brand-mark">S</div>
      <div><div className="brand-name">Sarkar SevaCheck</div><div className="brand-sub">{t.subtitle}</div></div>
    </div>
    <nav className="main-nav">
      {[["dashboard", t.dashboard],["ocr", t.ocr],["map", t.map],["reports", t.reports],["admin", t.admin]].map(([id, label]) =>
        <button key={id} className={page === id ? "nav-btn active" : "nav-btn"} onClick={() => setPage(id)}>{label}</button>
      )}
    </nav>
    <div className="header-actions">
      <button className="outline-btn" onClick={() => setLang(lang === "en" ? "hi" : "en")}>{lang === "en" ? t.hindi : t.english}</button>
      {user ? <button className="dark-btn" onClick={onLogout}>{t.logout}</button> : <button className="dark-btn" onClick={() => setPage("login")}>{t.login}</button>}
    </div>
  </header>;
}

function ServiceCard({ service, lang }) {
  const t = T[lang];
  const official = isOfficial(service), demo = isDemo(service), total = totalFee(service);
  return <article className="service-card">
    <div className="service-head">
      <div><h3>{service.name}</h3><p className="muted">{service.department}</p></div>
      <span className={`badge ${official ? "official" : demo ? "demo" : "verify"}`}>{official ? t.verified : demo ? t.demoBadge : t.verify}</span>
    </div>
    <p className="description">{service.description}</p>
    <div className="fee-grid">
      <div className="fee-box"><span>{t.gov}</span><strong>{money(service.government_fee)}</strong></div>
      <div className="fee-box"><span>{t.serviceCharge}</span><strong>{money(service.authorized_service_charge)}</strong></div>
      <div className="fee-box"><span>{t.other}</span><strong>{money(service.other_allowed_charge)}</strong></div>
      <div className="fee-box total"><span>{t.payable}</span><strong>{total == null ? t.awaiting : money(total)}</strong></div>
    </div>
    {official && <div className="proof official-text">✓ {t.verified} · {service.verified_on}</div>}
    {demo && <div className="proof demo-text">⚠ {t.demoWarning}</div>}
    {!official && !demo && <div className="proof verify-text">ⓘ Fee source must be verified before public use.</div>}
    <div className="card-actions">
      <a className="dark-btn link-btn" href={service.official_portal} target="_blank" rel="noreferrer">{t.apply}</a>
      <a className="outline-btn link-btn" href={service.source_url} target="_blank" rel="noreferrer">{t.feeSource}</a>
    </div>
    <div className="meta"><b>{t.processing}:</b> {service.processing_days} · <b>{t.documents}:</b> {service.documents}</div>
  </article>;
}

function Dashboard({ services, lang }) {
  const t = T[lang];
  const official = services.filter(isOfficial).length, demo = services.filter(isDemo).length;
  return <>
    <section className="hero"><span className="eyebrow">Citizen transparency prototype</span><h1>{t.before}</h1><p>{t.source}</p></section>
    <section className="stats">
      <div className="stat"><strong>{services.length}</strong><span>{t.total}</span></div>
      <div className="stat"><strong className="green">{official}</strong><span>{t.official}</span></div>
      <div className="stat"><strong className="amber">{demo}</strong><span>{t.demo}</span></div>
      <div className="stat"><strong>OCR</strong><span>Payment evidence check</span></div>
    </section>
    <div className="section-title"><div><h2>Government services</h2><p>{services.length} services · 20/20 demo records configured</p></div></div>
    {services.length === 0 ? <div className="empty">{t.noResults}</div> : <div className="service-list">{services.map(s => <ServiceCard key={s.id} service={s} lang={lang} />)}</div>}
    <section className="flow"><div className="flow-title"><span>{t.flow}</span><h2>Know → Apply → Pay → Verify → Report</h2></div><div className="flow-grid">{[t.know,t.applyStep,t.pay,t.verifyStep,t.report].map((x,i)=><div key={x}><small>0{i+1}</small><h3>{x}</h3><p>{t.flowText[i]}</p></div>)}</div></section>
    <div className="accuracy"><b>{t.accuracy}</b><p>{t.accuracyText}</p></div>
  </>;
}

function Login({ lang, setUser, setPage }) {
  const t = T[lang]; const [mobile, setMobile] = useState(""); const [name, setName] = useState(""); const [mode, setMode] = useState("login"); const [error, setError] = useState(""); const [loading, setLoading] = useState(false);
  async function submit(e) { e.preventDefault(); setError(""); if (!/^[6-9]\d{9}$/.test(mobile)) { setError("Enter a valid 10-digit Indian mobile number."); return; } try { setLoading(true); const fn = mode === "login" ? api.login : api.register; const data = await fn({mobile, name: name || "Citizen"}); localStorage.setItem("token", data.token); setUser(data.user); setPage("dashboard"); } catch (err) { setError(err.message); } finally { setLoading(false); } }
  return <div className="auth-card"><div className="eyebrow">Demo access</div><h2>{mode === "login" ? t.login : t.register}</h2><p className="muted">{t.loginHint}</p><form onSubmit={submit}>
    {mode === "register" && <label>{t.name}<input value={name} onChange={e=>setName(e.target.value)} placeholder="Your name" /></label>}
    <label>{t.mobile}<input inputMode="numeric" value={mobile} onChange={e=>setMobile(e.target.value.replace(/\D/g,"").slice(0,10))} placeholder="9876543210" /></label>
    {error && <div className="error">{error}</div>}
    <button className="dark-btn full" disabled={loading}>{loading ? t.loading : t.continue}</button>
  </form><button className="text-btn" onClick={()=>{setMode(mode === "login" ? "register" : "login");setError("")}}>{mode === "login" ? t.register : t.login}</button></div>;
}

function OCRPage({ services, lang, user, setPage }) {
  const t = T[lang];

  const [serviceId, setServiceId] = useState("");
  const [file, setFile] = useState(null);
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [notes, setNotes] = useState("");

  useEffect(() => {
    if (!serviceId && services.length) {
      setServiceId(
        String(services.find(hasFee)?.id || services[0].id)
      );
    }
  }, [services, serviceId]);

  const selected = services.find(
    s => String(s.id) === String(serviceId)
  );

  async function scan() {
    setError("");
    setResult(null);

    if (!file) {
      setError(t.noFile);
      return;
    }

    if (!selected) {
      setError(t.noService);
      return;
    }

    try {
      setBusy(true);

      const form = new FormData();
      form.append("file", file);
      form.append("service_id", String(selected.id));

      const data = await api.ocr(form);

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  async function submitReport() {
    if (!user) {
      setPage("login");
      return;
    }

    if (
      result?.extracted_amount === null ||
      result?.extracted_amount === undefined
    ) {
      setError("OCR amount is not available.");
      return;
    }

    try {
      setError("");

      const saved = await api.report({
        service_id: selected.id,
        amount_paid: Number(result.extracted_amount),
        extracted_amount: Number(result.extracted_amount),
        extracted_text: result.text || "",
        notes
      });

      setResult({
        ...result,
        report: saved
      });
    } catch (err) {
      setError(err.message);
    }
  }

  const comparison = result?.comparison;

  return (
    <div className="panel narrow">

      <div className="eyebrow">
        Payment evidence
      </div>

      <h2>{t.receiptTitle}</h2>

      <p className="muted">
        {t.receiptHint}
      </p>

      {/* SERVICE + RECEIPT UPLOAD */}
      <div className="form-grid">

        <label>
          {t.chooseService}

          <select
            value={serviceId}
            onChange={e => setServiceId(e.target.value)}
          >
            {services.map(s => (
              <option key={s.id} value={s.id}>
                {s.name}
                {isDemo(s) ? " — DEMO" : ""}
              </option>
            ))}
          </select>
        </label>

        <label>
          {t.chooseFile}

          <input
            type="file"
            accept="image/*"
            onChange={e =>
              setFile(e.target.files?.[0] || null)
            }
          />
        </label>

      </div>

      {/* SCAN BUTTON */}
      <button
        className="dark-btn"
        onClick={scan}
        disabled={busy}
      >
        {busy ? t.loading : t.runOCR}
      </button>

      {error && (
        <div className="error mt">
          {error}
        </div>
      )}

      {/* RESULT */}
      {result && (
        <div className="result-card">

          <div className="result-head">

            <h3>{t.result}</h3>

            <span
              className={`badge ${
                result.is_official
                  ? "official"
                  : result.is_demo
                  ? "demo"
                  : "verify"
              }`}
            >
              {result.is_official
                ? t.verified
                : result.is_demo
                ? t.demoBadge
                : t.verify}
            </span>

          </div>

          {/* AMOUNT COMPARISON */}
          <div className="result-grid">

            <div>
              <span>{t.extracted}</span>

              <strong>
                {result.extracted_amount == null
                  ? "Not detected"
                  : money(result.extracted_amount)}
              </strong>
            </div>

            <div>
              <span>{t.documented}</span>

              <strong>
                {result.documented_total == null
                  ? t.awaiting
                  : money(result.documented_total)}
              </strong>
            </div>

          </div>

          {/* DEMO WARNING */}
          {result.is_demo && (
            <div className="demo-note">
              ⚠ {t.demoCheck}
            </div>
          )}

          {/* COMPARISON RESULT */}
          {comparison === "ABOVE_DOCUMENTED_AMOUNT" && (
            <div className="alert red">
              ⚠ {t.compareAbove}
            </div>
          )}

          {comparison === "WITHIN_DOCUMENTED_AMOUNT" && (
            <div className="alert green-bg">
              ✓ {t.compareWithin}
            </div>
          )}

          {comparison === "NEEDS_FEE_VERIFICATION" && (
            <div className="alert amber-bg">
              ⓘ {t.comparisonUnavailable}
            </div>
          )}

          {/* OCR TEXT */}
          <details>
            <summary>OCR text</summary>

            <pre>
              {result.text || "No text detected"}
            </pre>
          </details>

          {/* CITIZEN NOTE */}
          <textarea
            value={notes}
            onChange={e => setNotes(e.target.value)}
            placeholder={t.note}
          />

          {/* SUBMIT REPORT */}
          <div className="submit-report-box">

            <button
              type="button"
              className="dark-btn submit-report-btn"
              onClick={submitReport}
              disabled={!!result.report}
            >
              {result.report
                ? `✓ ${t.reportSent}`
                : `📤 ${t.submitReport}`}
            </button>

          </div>

          {result.report && (
            <div className="success mt">
              ✓ {t.reportSent}
            </div>
          )}

        </div>
      )}

    </div>
  );
}

function Reports({ lang, setPage }) { const t=T[lang]; const [reports,setReports]=useState([]); const [loading,setLoading]=useState(true); const [error,setError]=useState(""); useEffect(()=>{api.myReports().then(x=>setReports(Array.isArray(x)?x:[])).catch(e=>setError(e.message)).finally(()=>setLoading(false));},[]); return <div className="panel"><div className="section-title"><div><div className="eyebrow">Evidence history</div><h2>{t.reportsTitle}</h2></div></div>{loading?<div className="empty">{t.loading}</div>:error?<div className="error">{error}. <button className="text-btn" onClick={()=>setPage("login")}>{t.login}</button></div>:!reports.length?<div className="empty">{t.noReports}</div>:<div className="report-list">{reports.map(r=><div className="report-row" key={r.id}><div><b>{r.service_name}</b><small>{new Date(r.created_at).toLocaleString()}</small></div><div><span>{t.paid}</span><strong>{money(r.amount_paid)}</strong></div><span className="status-pill">{r.status}</span><p>{r.notes}</p></div>)}</div>}</div> }

function MapPage({ services, lang }) {
  const t=T[lang]; const mapRef=useRef(null); const nodeRef=useRef(null); useEffect(()=>{if(!nodeRef.current||mapRef.current)return;const map=L.map(nodeRef.current,{scrollWheelZoom:true}).setView([30.2,79.1],7);L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",{attribution:"© OpenStreetMap contributors"}).addTo(map);DISTRICTS.forEach(([name,lat,lng])=>{L.circleMarker([lat,lng],{radius:7,weight:2}).addTo(map).bindPopup(`<b>${name}</b><br>${services.length} services`)});mapRef.current=map;setTimeout(()=>map.invalidateSize(),250);return()=>{map.remove();mapRef.current=null}},[services.length]); return <div className="panel"><div className="section-title"><div><div className="eyebrow">OpenStreetMap</div><h2>{t.demoMap}</h2><p>{t.mapNote}</p></div></div><div ref={nodeRef} className="map"></div><div className="district-grid">{DISTRICTS.map(([d])=><div className="district" key={d}><b>{d}</b><span>{services.length} {t.servicesAvailable}</span></div>)}</div></div> }

function Admin({ services, lang, reload }) { const t=T[lang]; const [editing,setEditing]=useState(null); const [message,setMessage]=useState(""); const [stats,setStats]=useState(null); const [reportStats,setReportStats]=useState(null); const blank={department:"Revenue Department",name:"",description:"DEMO DATA: Synthetic hackathon test amount. Not an official government fee.",government_fee:0,authorized_service_charge:0,other_allowed_charge:0,processing_days:"Demo processing time",documents:"Check official portal.",official_portal:"https://eservices.uk.gov.in/",source_url:"https://it.uk.gov.in/apuni-sarkar/",source_document:"",fee_status:"DEMO_DATA",verified_on:"",office_name:"Relevant Uttarakhand office",state:"Uttarakhand"}; const [form,setForm]=useState(blank);
  useEffect(()=>{Promise.all([api.adminStats(),api.reportSummary()]).then(([a,r])=>{setStats(a);setReportStats(r)}).catch(()=>{})},[services]);
  const begin=(s)=>{setEditing(s.id);setForm({...s})}; const change=e=>setForm({...form,[e.target.name]:e.target.value});
  async function save(){try{const payload={...form,government_fee:Number(form.government_fee),authorized_service_charge:Number(form.authorized_service_charge),other_allowed_charge:Number(form.other_allowed_charge),latitude:form.latitude?Number(form.latitude):null,longitude:form.longitude?Number(form.longitude):null};if(editing)await api.adminUpdate(editing,payload);else await api.adminCreate(payload);setMessage(editing?t.saved:t.added);setEditing(null);setForm(blank);await reload()}catch(e){setMessage(e.message)}}
  async function del(id){if(!window.confirm(t.confirmDelete))return;try{await api.adminDelete(id);setMessage(t.deleted);await reload()}catch(e){setMessage(e.message)}}
  return <div className="panel"><div className="section-title"><div><div className="eyebrow">Administrator</div><h2>{t.adminTitle}</h2></div></div>{stats&&<div className="admin-stats"><div className="mini"><b>{stats.total_services}</b><span>{t.total}</span></div><div className="mini"><b>{stats.official_verified}</b><span>{t.official}</span></div><div className="mini"><b>{stats.demo_data}</b><span>{t.demo}</span></div><div className="mini"><b>{reportStats?.total||0}</b><span>{t.totalReports}</span></div><div className="mini"><b>{reportStats?.above_verified_total||0}</b><span>{t.excessOfficial}</span></div><div className="mini"><b>{reportStats?.above_demo_total||0}</b><span>{t.excessDemo}</span></div></div>}
    <div className="admin-form"><h3>{editing?t.edit:t.create}</h3>{["name","department","government_fee","authorized_service_charge","other_allowed_charge","processing_days","documents","source_url","official_portal","office_name"].map(n=><label key={n}>{n.replaceAll("_"," ")}<input name={n} value={form[n] ?? ""} onChange={change}/></label>)}<label className="full-row">description<textarea name="description" value={form.description} onChange={change}/></label><label>fee status<select name="fee_status" value={form.fee_status} onChange={change}><option value="DEMO_DATA">DEMO_DATA</option><option value="VERIFIED_OFFICIAL">VERIFIED_OFFICIAL</option><option value="VERIFY_FROM_OFFICIAL_ORDER">VERIFY_FROM_OFFICIAL_ORDER</option></select></label><div className="admin-actions"><button className="dark-btn" onClick={save}>{t.save}</button>{editing&&<button className="outline-btn" onClick={()=>{setEditing(null);setForm(blank)}}>{t.cancel}</button>}</div></div>{message&&<div className="success mt">{message}</div>}
    <div className="admin-list">{services.map(s=><div className="admin-row" key={s.id}><div><b>{s.name}</b><small>{s.fee_status} · {money(totalFee(s))}</small></div><div className="row-actions"><button className="outline-btn small" onClick={()=>begin(s)}>{t.edit}</button><button className="danger-btn small" onClick={()=>del(s.id)}>{t.delete}</button></div></div>)}</div></div> }

export default function App(){const [lang,setLang]=useState("en");const [page,setPage]=useState("dashboard");const [services,setServices]=useState([]);const [query,setQuery]=useState("");const [user,setUser]=useState(null);const [loading,setLoading]=useState(true);const [loadError,setLoadError]=useState(""); const t=T[lang];
  const load=async()=>{try{setLoading(true);setLoadError("");setServices(await api.services(query))}catch(e){setLoadError(e.message)}finally{setLoading(false)}};
  useEffect(()=>{load()},[query]); useEffect(()=>{const token=localStorage.getItem("token");if(token)api.me().then(setUser).catch(()=>localStorage.removeItem("token"))},[]);
  function logout(){localStorage.removeItem("token");setUser(null);setPage("dashboard")};
  function guarded(target){if(target==="admin"){if(!user){setPage("login");return}if(user.mobile!==DEMO_ADMIN && !user.is_admin){alert(t.adminOnly);return}}if(target==="reports"&&!user){setPage("login");return}setPage(target)};
  return <div className="app"><Header lang={lang} setLang={setLang} user={user} onLogout={logout} page={page} setPage={guarded}/><main className="container"><div className="toolbar">{page==="dashboard"&&<input className="search" value={query} onChange={e=>setQuery(e.target.value)} placeholder={t.search}/>} </div>{loading&&page==="dashboard"?<div className="empty">{t.loading}</div>:loadError&&page==="dashboard"?<div className="empty"><h3>{t.apiError}</h3><p>{loadError}</p><button className="dark-btn" onClick={load}>Retry</button></div>:page==="dashboard"?<Dashboard services={services} lang={lang}/>:page==="login"?<Login lang={lang} setUser={setUser} setPage={setPage}/>:page==="ocr"?<OCRPage services={services} lang={lang} user={user} setPage={setPage}/>:page==="reports"?<Reports lang={lang} setPage={setPage}/>:page==="map"?<MapPage services={services} lang={lang}/>:page==="admin"?<Admin services={services} lang={lang} reload={load}/>:null}</main><footer>Sarkar SevaCheck · Hackathon prototype · Citizen transparency layer, not a replacement for government</footer></div>}


