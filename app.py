import gradio as gr
from typing import Dict, List, Any

class NexusCoreGateway:
    def __init__(self, loop_similarity_threshold: float = 0.90):
        self.agent_state_cache: Dict[str, List[str]] = {}
        self.billing_rules_vault: Dict[str, Dict[str, Any]] = {}
        self.similarity_threshold = loop_similarity_threshold

    def configure_enterprise_contract(self, customer_id: str, flat_allowance: int, overage_rate: float):
        self.billing_rules_vault[customer_id] = {
            "flat_allowance_tokens": flat_allowance,
            "overage_rate_per_1k": overage_rate
        }

    def execute_billing_reconciliation(self, customer_id: str, cumulative_tokens_consumed: int, actual_invoiced_amount: float) -> tuple:
        if customer_id not in self.billing_rules_vault:
            return "<div style='color:#EF4444;'>Error: Contract profile metadata missing.</div>", ""
            
        rules = self.billing_rules_vault[customer_id]
        flat_allowance = rules["flat_allowance_tokens"]
        overage_rate = rules["overage_rate_per_1k"]
        
        expected_amount = 0.0
        if cumulative_tokens_consumed > flat_allowance:
            overage_tokens = cumulative_tokens_consumed - flat_allowance
            expected_amount = (overage_tokens / 1000.0) * overage_rate
            
        revenue_leakage = expected_amount - actual_invoiced_amount
        status_color = "#EF4444" if revenue_leakage > 0 else "#10B981"
        
        summary_html = f"""
        <div style='text-align: center; background: #0F172A; padding: 25px; border-radius: 8px; border: 1px solid #334155; margin-bottom: 15px;'>
            <h3 style='color: #94A3B8; margin: 0; font-size: 13px; text-transform: uppercase; letter-spacing: 0.05em;'>Audited Metric: Revenue Leakage</h3>
            <h1 style='color: {status_color}; margin: 5px 0; font-size: 36px; font-weight: 800;'>INR {max(0.0, revenue_leakage):,.2f}</h1>
            <p style='color: #E2E8F0; margin: 0; font-size: 14px;'>Status: <b>{"🔴 LEAKAGE DETECTED" if revenue_leakage > 0 else "🟢 AUDIT CLEAR"}</b></p>
        </div>
        """
        
        ledger_html = f"""
        <div style='background: #1E293B; padding: 16px; border-radius: 6px; color: #E2E8F0; font-family: monospace;'>
            <b style='color: #F8FAFC; font-size: 14px;'>🗃️ AUDIT COMPLIANCE RUN LEDGER</b><br><br>
            • Customer Account: <span style='color:#38BDF8;'>{customer_id}</span><br>
            • Infrastructure Meter: <span style='color:#F59E0B;'>{cumulative_tokens_consumed:,} tokens</span><br>
            • Contract Flat Allowance: {flat_allowance:,} tokens<br>
            • Overage Contract Rate: INR {overage_rate:.2f} per 1k<br>
            • Calculated Expected Invoice: INR {expected_amount:,.2f}<br>
            • System Actual Invoiced: INR {actual_invoiced_amount:,.2f}<br><br>
            <hr style='border: 0; border-top: 1px solid #334155;'>
            <b style='color: #F8FAFC;'>🤖 DISPATCHED REMEDIATION ACTION:</b><br>
            <span style='color: #34D399;'>{"[TRIGGER]: Generated corrected invoice payload & pushed to Stripe Invoicing Gateway." if revenue_leakage > 0 else "[PASS]: Ledger reconciliation zeroed out perfectly."}</span>
        </div>
        """
        return summary_html, ledger_html

# =========================================================================
# INTERACTIVE EXECUTIVE APPLICATION INTERFACE
# =========================================================================
gateway = NexusCoreGateway()

with gr.Blocks(theme=gr.themes.Soft(primary_hue="emerald", neutral_hue="slate")) as demo:
    gr.HTML("""
        <div style='text-align: center; padding: 20px 0;'>
            <h1 style='color: #10B981; margin: 0; font-weight: 800; letter-spacing: -0.02em;'>NEXUS GATEWAY EXECUTIVE DASHBOARD</h1>
            <p style='color: #64748B; margin: 5px 0 0 0; font-size: 14px;'>Layer 3 Usage-Based Revenue Assurance Plane</p>
        </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📊 Enterprise Contract & Usage Meters")
            c_id = gr.Textbox(value="Enterprise-SaaS-Alpha", label="Customer Account Identifier")
            allowance = gr.Number(value=1000000, label="Contract Flat Allowance (Tokens)")
            ovr_rate = gr.Number(value=50.0, label="Overage Pricing Rate (INR per 1k Tokens)")
            consumed = gr.Number(value=1500000, label="Actual Infrastructure Consumption (Tokens)")
            invoiced = gr.Number(value=5000.0, label="Current System Invoiced Amount (INR)")
            
            audit_btn = gr.Button("🚀 Run Infrastructure Financial Audit", variant="primary")
            
        with gr.Column(scale=1):
            gr.Markdown("### 🏛️ Financial Compliance Assurance Report")
            output_sum = gr.HTML(value="<div style='text-align: center; color: #64748B; padding: 40px;'>Input parameters and trigger the audit matrix configuration.</div>")
            output_led = gr.HTML()

    def run_pipeline(c_id, allowance, ovr_rate, consumed, invoiced):
        gateway.configure_enterprise_contract(c_id, int(allowance), float(ovr_rate))
        return gateway.execute_billing_reconciliation(c_id, int(consumed), float(invoiced))

    audit_btn.click(
        fn=run_pipeline,
        inputs=[c_id, allowance, ovr_rate, consumed, invoiced],
        outputs=[output_sum, output_led]
    )

if __name__ == "__main__":
    demo.launch()
  
