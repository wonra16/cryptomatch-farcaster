"""
Advanced Matchmaking Algorithm
Calculates compatibility scores with multiple factors
"""
from typing import Dict, List, Optional
from personality import PersonalityAnalyzer, PersonalityType, RiskLevel
from comedy_generator import comedy_generator
from image_generator import image_generator
import random


class MatchmakingEngine:
    """Advanced crypto matchmaking engine"""
    
    def __init__(self):
        self.personality_analyzer = PersonalityAnalyzer()
        self.weights = {
            "personality_base": 0.30,    # Base personality compatibility
            "token_overlap": 0.25,        # Common token interests
            "risk_tolerance": 0.20,       # Risk level match
            "trait_similarity": 0.15,     # Similar behavioral traits
            "community_vibe": 0.10        # Overall community fit
        }
    
    async def find_matches(
        self,
        user_personality: Dict,
        potential_matches: List[Dict],
        top_n: int = 3
    ) -> List[Dict]:
        """
        Find top N matches for a user
        """
        scored_matches = []
        
        for match_candidate in potential_matches:
            compatibility = await self.calculate_compatibility(
                user_personality,
                match_candidate
            )
            scored_matches.append({
                "match": match_candidate,
                "compatibility": compatibility
            })
        
        # Sort by score descending
        scored_matches.sort(key=lambda x: x["compatibility"]["total_score"], reverse=True)
        
        return scored_matches[:top_n]
    
    async def calculate_compatibility(
        self,
        user1: Dict,
        user2: Dict
    ) -> Dict:
        """
        Calculate detailed compatibility between two users
        """
        # Get personality profiles
        profile1 = user1.get("profile", {})
        profile2 = user2.get("profile", {})
        
        personality1 = user1.get("personality_type", PersonalityType.BITCOIN_MAXI)
        personality2 = user2.get("personality_type", PersonalityType.BITCOIN_MAXI)
        
        # Get compatibility factors
        factors = self.personality_analyzer.get_compatibility_factors(
            personality1,
            personality2
        )
        
        # Calculate weighted score
        scores = {
            "personality_base": factors["base_compatibility"],
            "token_overlap": factors["token_compatibility"],
            "risk_tolerance": factors["risk_compatibility"],
            "trait_similarity": self._calculate_trait_similarity(profile1, profile2),
            "community_vibe": random.randint(60, 95)  # Placeholder for real community data
        }
        
        # Calculate total weighted score
        total_score = sum(
            scores[key] * self.weights[key]
            for key in scores.keys()
        )
        
        # Round to integer
        total_score = int(round(total_score))
        
        # Determine match level
        if total_score >= 80:
            match_level = "high_match"
        elif total_score >= 60:
            match_level = "medium_match"
        else:
            match_level = "low_match"
        
        # Generate comedy and date idea
        comedy = await comedy_generator.generate_match_comedy(
            profile1,
            profile2,
            total_score,
            match_level
        )
        
        date_idea = await comedy_generator.generate_date_idea(profile1, profile2)
        
        # Generate result image
        image_url = image_generator.generate_match_image(
            profile1,
            profile2,
            total_score,
            match_level,
            comedy
        )
        
        return {
            "total_score": total_score,
            "match_level": match_level,
            "breakdown": scores,
            "common_tokens": factors["common_tokens"],
            "comedy": comedy,
            "date_idea": date_idea,
            "image_url": image_url,
            "personality1": {
                "type": personality1,
                "title": profile1.get("title", "Unknown"),
                "emoji": profile1.get("emoji", "💫")
            },
            "personality2": {
                "type": personality2,
                "title": profile2.get("title", "Unknown"),
                "emoji": profile2.get("emoji", "💫")
            }
        }
    
    def _calculate_trait_similarity(self, profile1: Dict, profile2: Dict) -> float:
        """Calculate similarity between personality traits"""
        traits1 = set(profile1.get("traits", []))
        traits2 = set(profile2.get("traits", []))
        
        if not traits1 or not traits2:
            return 50.0
        
        # Calculate Jaccard similarity
        intersection = len(traits1 & traits2)
        union = len(traits1 | traits2)
        
        similarity = (intersection / union) * 100 if union > 0 else 0
        
        return similarity
    
    async def generate_match_result(
        self,
        user_fid: str,
        match_fid: str,
        user_name: str = "You",
        match_name: str = "Your Match"
    ) -> Dict:
        """
        Generate complete match result for Frame display
        """
        # Analyze both users
        user_analysis = self.personality_analyzer.analyze_user()
        match_analysis = self.personality_analyzer.analyze_user()
        
        # Calculate compatibility
        compatibility = await self.calculate_compatibility(
            user_analysis,
            match_analysis
        )
        
        # Generate share text
        share_text = await comedy_generator.generate_viral_share_text(
            user_name,
            match_name,
            compatibility["total_score"],
            compatibility["comedy"]
        )
        
        return {
            "user": {
                "fid": user_fid,
                "name": user_name,
                "personality": user_analysis
            },
            "match": {
                "fid": match_fid,
                "name": match_name,
                "personality": match_analysis
            },
            "compatibility": compatibility,
            "share_text": share_text,
            "timestamp": "2025-10-23T00:00:00Z"
        }


# Singleton instance
matchmaking_engine = MatchmakingEngine()
