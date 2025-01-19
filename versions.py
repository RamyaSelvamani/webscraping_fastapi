from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Version, User
from schemas import VersionCreate, VersionResponse
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from utils import SECRET_KEY, ALGORITHM
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
from typing import List

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

version_pattern = re.compile(r"(\d+\.\d+)")
date_pattern = re.compile(r"\d{4}-\d{2}-\d{2}")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/scrape")
def scrape_versions(url: str = "https://docs.rockylinux.org/release_notes/"):
    """
    Scrape versions and release dates from the specified URL and return them directly from the browser.
    """
    try:
        # Fetch the page content
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Locate all relevant sections
        release_sections = soup.find_all("h2")
        scraped_versions = []

        for section in release_sections:
            version_header = section.get_text(strip=True)

            if "Rocky" in version_header:  # Process sections related to Rocky Linux
                release_table = section.find_next("table")
                if release_table:
                    for row in release_table.find_all("tr")[1:]:  # Skip the header row
                        columns = row.find_all("td")
                        if len(columns) >= 2:
                            release_version_raw = columns[0].get_text(strip=True)
                            release_date_raw = columns[1].get_text(strip=True)

                            # Match version and date patterns
                            version_match = version_pattern.search(release_version_raw)
                            date_match = date_pattern.search(release_date_raw)
                            if version_match and date_match:
                                scraped_versions.append({
                                    "minor_version": version_match.group(1),
                                    "release_date": date_match.group()
                                })

        return scraped_versions

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

@router.get("/", response_model=list[VersionResponse])
def get_versions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get all versions associated with the current user.
    """
    return db.query(Version).filter(Version.user_id == current_user.id).all()

@router.post("/", response_model=List[VersionResponse])
def add_versions(
    versions: List[VersionCreate],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Add multiple version entries for the authenticated user.

    """
    added_versions = []
    try:
        for version in versions:
        
            new_version = Version(
            minor_version=version.minor_version,
            release_date=version.release_date,
            user_id=current_user.id,  
        )
            db.add(new_version)
            added_versions.append(new_version)

    # Commit the transaction
            db.commit()

    # Refresh added versions for returning in response
        for version in added_versions:
            db.refresh(version)

        return added_versions
    finally:
        db.close()


@router.put("/{version_id}", response_model=VersionResponse)
def update_version(version_id: int, updated_version: VersionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Update an existing version entry by version ID.
    """
    version = db.query(Version).filter(Version.id == version_id, Version.user_id == current_user.id).first()
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")
    version.minor_version = updated_version.minor_version
    version.release_date = updated_version.release_date
    db.commit()
    db.refresh(version)
    return version


@router.delete("/{version_id}")
def delete_version(version_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Delete a version entry by version ID.
    """
    version = db.query(Version).filter(Version.id == version_id, Version.user_id == current_user.id).first()
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")
    db.delete(version)
    db.commit()
    return {"message": "Version deleted successfully"}


@router.get("/get_minor_version_all/{minor_version}")
def get_minor_version_all(minor_version: str, db: Session = Depends(get_db), current_user:User=Depends(get_current_user)):
    minor_version_all=db.query(Version).filter(Version.minor_version==minor_version,Version.user_id == current_user.id).all()
    return minor_version_all
                          