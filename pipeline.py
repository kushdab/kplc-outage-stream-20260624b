import re
import logging
import json
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class OutageNotice(BaseModel):
    region: str
    county: str
    area: List[str]
    date: str
    time_window: str
    timestamp: datetime = Field(default_factory=datetime.now)

class OutageProcessor:
    """Processes raw text notices into structured data objects."""
    
    def __init__(self):
        # Simulation of KPLC notice patterns
        self.region_pattern = re.compile(r"REGION:\s*(.*?)\s*COUNTY:", re.IGNORECASE)
        self.county_pattern = re.compile(r"COUNTY:\s*(.*?)\s*AREA:", re.IGNORECASE)
        self.area_pattern = re.compile(r"AREA:\s*(.*?)(?=\s*DATE:|$)", re.IGNORECASE)
        self.date_pattern = re.compile(r"DATE:\s*(.*?)\s*TIME:", re.IGNORECASE)
        self.time_pattern = re.compile(r"TIME:\s*(.*?)(?=\s*REGION:|$)", re.IGNORECASE)

    def parse_raw_text(self, raw_content: str) -> List[OutageNotice]:
        """Splits and parses a batch of notices."""
        notices = []
        # In real scenario, KPLC notices are grouped by blocks
        blocks = raw_content.split("---SEPARATOR---")
        
        for block in blocks:
            try:
                region = self.region_pattern.search(block)
                county = self.county_pattern.search(block)
                area_raw = self.area_pattern.search(block)
                date_val = self.date_pattern.search(block)
                time_val = self.time_pattern.search(block)

                if all([region, county, area_raw, date_val, time_val]):
                    areas = [a.strip() for a in area_raw.group(1).split(",")]
                    notice = OutageNotice(
                        region=region.group(1).strip(),
                        county=county.group(1).strip(),
                        area=areas,
                        date=date_val.group(1).strip(),
                        time_window=time_val.group(1).strip()
                    )
                    notices.append(notice)
            except Exception as e:
                logger.error(f"Failed to parse block: {e}")
        
        return notices

class OutagePipeline:
    """Orchestrates data ingestion and transformation."""

    def __init__(self):
        self.processor = OutageProcessor()

    def fetch_mock_data(self) -> str:
        """Simulates fetching data from KPLC's public notices endpoint."""
        return (
            "REGION: NAIROBI COUNTY: NAIROBI AREA: Part of Westlands, Sarit Centre, Parklands DATE: 24.06.2026 TIME: 09:00 AM - 5:00 PM"
            "---SEPARATOR---"
            "REGION: COAST COUNTY: MOMBASA AREA: Nyali, Bamburi, Links Rd DATE: 25.06.2026 TIME: 08:30 AM - 4:30 PM"
            "---SEPARATOR---"
            "REGION: CENTRAL RIFT COUNTY: NAKURU AREA: Nakuru CBD, Milimani, Blankets DATE: 24.06.2026 TIME: 09:00 AM - 5:00 PM"
        )

    def run(self):
        logger.info("Starting KPLC Outage Stream Pipeline...")
        
        # 1. Ingest
        raw_data = self.fetch_mock_data()
        logger.info("Data successfully ingested from source.")

        # 2. Process
        parsed_notices = self.processor.parse_raw_text(raw_data)
        logger.info(f"Processed {len(parsed_notices)} outage notices.")

        # 3. Filter & Output (Logic to find today's outages)
        today_str = "24.06.2026" # Mocking fixed date for demonstration
        updates = [n for n in parsed_notices if n.date == today_str]

        print("\n--- REAL-TIME OUTAGE UPDATES ---")
        for update in updates:
            print(f"[!] {update.county} ({update.region})")
            print(f"    Areas: {', '.join(update.area)}")
            print(f"    Window: {update.time_window}\n")

        # 4. Save to JSON for downstream consumers
        with open("latest_outages.json", "w") as f:
            json.dump([n.dict() for n in parsed_notices], f, indent=4, default=str)
        logger.info("Pipeline execution complete. Results saved to latest_outages.json.")

if __name__ == "__main__":
    pipeline = OutagePipeline()
    pipeline.run()