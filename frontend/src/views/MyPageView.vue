<template>
  <div class="page">
    <MyPageProfileCard 
      :user="user" 
      @edit="openEdit = true" 
      @open-follow="onOpenFollowModal"
    />
    
    <MyPageTabs v-model="tab" />

    <div v-if="tab === 'vault'" class="content">
      <MyPageSection 
        title="코멘트 영화 (작성한)" 
        :moreLink="{ name: 'mypage-grid', params: { type: 'commented' }}"
        :isEmpty="commentedList.length === 0"
        emptyMsg="작성한 코멘트가 없습니다."
      >
        <MovieCard v-for="item in commentedList.slice(0, 5)" :key="item.id" :movie="item.movie" />
      </MyPageSection>

      <MyPageSection 
        title="좋아요 한 영화" 
        :moreLink="{ name: 'mypage-grid', params: { type: 'movie_likes' }}"
        :isEmpty="movieLikesList.length === 0"
        emptyMsg="좋아요 한 영화가 없습니다."
      >
        <MovieCard v-for="item in movieLikesList.slice(0, 5)" :key="item.id" :movie="item" />
      </MyPageSection>

      <MyPageSection 
        title="보고싶은 영화" 
        :moreLink="{ name: 'mypage-grid', params: { type: 'wish' }}"
        :isEmpty="wishList.length === 0"
        emptyMsg="보고싶은 영화가 없습니다."
      >
        <MovieCard v-for="item in wishList.slice(0, 5)" :key="item.id" :movie="item.movie" />
      </MyPageSection>
    </div>

    <div v-else class="content">
      <MyPageSection 
        title="인물 (자신이 좋아요를 누른)" 
        :moreLink="{ name: 'mypage-grid', params: { type: 'liked_people' }}"
        :isEmpty="likedPeople.length === 0"
        emptyMsg="좋아요한 인물이 없습니다."
      >
        <PersonCard 
          v-for="p in likedPeople.slice(0, 5)" 
          :key="p.tmdb_id" 
          :person="p" 
          @toggle-like="handleUnlikePerson" 
        />
      </MyPageSection>

      <MyPageSection 
        title="코멘트 (자신이 좋아요를 누른)" 
        :moreLink="{ name: 'mypage-grid', params: { type: 'liked_reviews' }}"
        :isEmpty="likedReviews.length === 0"
        emptyMsg="좋아요한 코멘트가 없습니다."
      >
        <ReviewCard 
          v-for="r in likedReviews.slice(0, 5)" 
          :key="r.id" 
          :review="r" 
          @click="openReviewModal(r)"
          style="cursor: pointer;"
        />
      </MyPageSection>
    </div>

    <ProfileEditModal v-if="openEdit" :user="user" @close="openEdit = false" @saved="onProfileSaved" />

    <ReviewDetailModal 
      v-if="isReviewModalOpen" 
      :review="selectedReview" 
      @close="isReviewModalOpen = false" 
    />

    <UserListModal 
      v-if="isUserModalOpen"
      :title="userModalTitle"
      :users="userModalList"
      @close="isUserModalOpen = false"
    />
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
// ✅ [추가] fetchFollowList 임포트
import { fetchMyActivity, fetchMyLikes, togglePersonLike, fetchMyLikedPeople, fetchFollowList } from '@/api/comet' 

import MyPageProfileCard from '@/components/mypage/MyPageProfileCard.vue'
import MyPageTabs from '@/components/mypage/MyPageTabs.vue'
import MyPageSection from '@/components/mypage/MyPageSection.vue'
import MovieCard from '@/components/movie/MovieCard.vue'
import PersonCard from '@/components/movie/PersonCard.vue' 
import ReviewCard from '@/components/review/ReviewCard.vue'
import ProfileEditModal from '@/components/user/ProfileEditModal.vue' 
import ReviewDetailModal from '@/components/review/ReviewDetailModal.vue'
// ✅ [추가] 유저 리스트 모달 임포트
import UserListModal from '@/components/mypage/UserListModal.vue'

const auth = useAuthStore()
const user = computed(() => auth.user)

const tab = ref('vault')
const openEdit = ref(false)

const isReviewModalOpen = ref(false)
const selectedReview = ref(null)

// ✅ [추가] 유저 모달 관련 상태
const isUserModalOpen = ref(false)
const userModalTitle = ref('')
const userModalList = ref([])

const commentedList = ref([])
const movieLikesList = ref([])
const wishList = ref([])
const likedPeople = ref([])
const likedReviews = ref([])

function onProfileSaved(updatedUser) {
  auth.user = { ...auth.user, ...updatedUser }
}

async function handleUnlikePerson(person) {
  likedPeople.value = likedPeople.value.filter(p => p.tmdb_id !== person.tmdb_id)
  try {
    await togglePersonLike(person.tmdb_id)
  } catch (e) {
    console.error('취소 실패', e)
    alert('오류가 발생했습니다.')
  }
}

function openReviewModal(review) {
  selectedReview.value = review
  isReviewModalOpen.value = true
}

// ✅ [추가] 팔로워/팔로잉 모달 열기 함수
async function onOpenFollowModal(type) {
  // 1. 제목 설정
  userModalTitle.value = (type === 'followers') ? '팔로워' : '팔로잉'
  userModalList.value = [] // 초기화
  isUserModalOpen.value = true // 모달 열기

  // 2. API 호출
  try {
    const list = await fetchFollowList(user.value.username, type)
    userModalList.value = list
  } catch (e) {
    console.error("팔로우 리스트 로드 실패", e)
  }
}

onMounted(async () => {
  try {
    const [
      commented, 
      movieLikes, 
      wish, 
      people, 
      reviews
    ] = await Promise.all([
      fetchMyActivity({ status: 'commented', sort: 'latest' }),
      fetchMyLikes('movie'),
      fetchMyActivity({ status: 'wish', sort: 'latest' }),
      fetchMyLikedPeople(), 
      fetchMyActivity({ status: 'liked', sort: 'latest' })
    ])
    
    commentedList.value = commented || []
    movieLikesList.value = movieLikes || []
    wishList.value = wish || []
    likedPeople.value = people || []
    likedReviews.value = reviews || []

  } catch (error) {
    console.error("마이페이지 데이터 로드 실패:", error)
  }
})
</script>

<style scoped>
.page { max-width: 1100px; margin: 0 auto; padding: 30px 14px; padding-bottom: 100px; }
</style>