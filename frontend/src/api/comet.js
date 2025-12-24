// frontend/src/api/comet.js
import api from './axios'

// =========================
// 공통: Authorization 헤더 (인터셉터로 이미 붙이면 이거 없어도 됨)
// =========================
function authConfig(extra = {}) {
  const token = localStorage.getItem('access')
  if (!token) return extra
  return {
    ...extra,
    headers: {
      ...(extra.headers || {}),
      Authorization: `Bearer ${token}`,
    },
  }
}

// =========================
// movies
// =========================
export async function fetchHomeSections(page = 1) {
  const res = await api.get('/movies/home/', { params: { page } })
  return res.data
}

export async function fetchMovies(params = {}) {
  // ✅ 백엔드가 /movies/list/
  const res = await api.get('/movies/list/', { params })
  return res.data
}

export async function fetchGenres() {
  const res = await api.get('/movies/genres/')
  return res.data
}

export async function fetchMovieDetail(tmdbId) {
  const res = await api.get(`/movies/${tmdbId}/`)
  return res.data
}

export async function searchMulti(q, page = 1) {
  const res = await api.get('/movies/search/', { params: { q, page } })
  return res.data
}

export async function fetchPersonDetail(tmdbId) {
  const res = await api.get(`/movies/people/${tmdbId}/`)
  return res.data
}

// =========================
// reviews
// =========================
export async function fetchRecentReviews(limit = 12) {
  const res = await api.get('/reviews/recent/', { params: { limit } })
  return res.data
}

export async function fetchMovieReviews(tmdbId) {
  const res = await api.get(`/reviews/movie/${tmdbId}/`)
  return res.data
}

export async function createMovieReview(tmdbId, payload) {
  const res = await api.post(`/reviews/movie/${tmdbId}/create/`, payload)
  return res.data
}

export async function updateReview(reviewId, payload) {
  const res = await api.put(`/reviews/${reviewId}/`, payload)
  return res.data
}

export async function deleteReview(reviewId) {
  const res = await api.delete(`/reviews/${reviewId}/`)
  return res.data
}

export async function toggleReviewLike(reviewId) {
  const res = await api.post(`/reviews/${reviewId}/like/`)
  return res.data
}


// =========================
// accounts
// =========================
export async function signup(payload) {
  const res = await api.post('/auth/signup/', payload)
  return res.data
}

export async function login(payload) {
  const res = await api.post('/auth/login/', payload)
  return res.data
}

export async function fetchMe() {
  const res = await api.get('/auth/me/')
  return res.data
}



export async function updateMyTheme(theme) {
  const res = await api.patch('/auth/me/theme/', { theme })
  return res.data
}

export async function fetchUserProfile(username) {
  const res = await api.get(`/auth/users/${encodeURIComponent(username)}/`)
  return res.data
}

export async function toggleFollow(username) {
  const res = await api.post(`/auth/users/${encodeURIComponent(username)}/follow/`)
  return res.data
}

// =========================
// recommends (취향분석/추천)
// =========================

// 1) AI 챗봇(취향분석/맞춤추천 공용)
export async function postTasteChat(payload) {
  const { data } = await api.post('/recommends/ai/', payload, {
    headers: authHeaders(),
  })
  return data
}


// 2) 장르 추천
// GET /recommends/genres/
export async function fetchGenreRecommends(params = {}) {
  const res = await api.get('/recommends/genres/', authConfig({ params }))
  return res.data
}

// 3) 인물 추천
// GET /recommends/people/
export async function fetchPersonRecommends(params = {}) {
  const res = await api.get('/recommends/people/', authConfig({ params }))
  return res.data
}

// 4) 유저 추천
// GET /recommends/users/
export async function fetchUserRecommends(params = {}) {
  const res = await api.get('/recommends/users/', authConfig({ params }))
  return res.data
}


function authHeaders() {
  const token = localStorage.getItem('access')
  return token ? { Authorization: `Bearer ${token}` } : {}
}


// 검색

export const searchComet = (params) => {
  return api.get('/movies/search/', { params })
    .then(res => res.data)
}

// =========================
// (taste page)
// =========================
export async function fetchTasteDNA() {
  const { data } = await api.get('/recommends/taste/')
  return data
}









// =========================
// 마이페이지
// =========================
export async function fetchMyActivity(params = {}) {
  const res = await api.get('/reviews/my/', authConfig({ params }))
  return res.data
}

// [추가] 좋아요한 인물/장르 가져오기
export async function fetchMyLikes(type) {
  const res = await api.get('/movies/likes/', authConfig({ params: { type } }))
  return res.data
}


// export async function updateMyProfile(payload) {
//   const res = await api.patch('/auth/me/profile/', payload)
//   return res.data
// } 이거 수정 할게요 
export async function updateMyProfile(formData) {
  // 파일 전송을 위해 Content-Type 헤더를 multipart/form-data로 설정하는 것은
  // axios가 FormData를 감지하면 자동으로 처리하므로 별도 설정 불필요할 수 있으나,
  // 안전하게 authConfig 내부 동작 확인 필요. 보통은 그냥 보내면 됨.
  const res = await api.patch('/accounts/profile/', formData, authConfig()) 
  return res.data
}






// 영화 디테일 페이지 
// [완벽 구현] 비슷한 영화 API 호출
export async function fetchSimilarMovies(tmdbId) {
  try {
    const res = await api.get(`/movies/${tmdbId}/similar/`)
    return res.data
  } catch (e) {
    console.warn("Similar fetch failed", e)
    return []
  }
}

// [추가] 영화 좋아요 토글
export async function toggleMovieLike(tmdbId) {
  const res = await api.post(`/movies/${tmdbId}/like/`, {}, authConfig())
  return res.data
}






// [추가] 대댓글 목록 가져오기
export async function fetchReviewComments(reviewId) {
  const res = await api.get(`/reviews/${reviewId}/comments/`)
  return res.data
}

// [추가] 대댓글 작성하기
export async function createReviewComment(reviewId, content) {
  const res = await api.post(`/reviews/${reviewId}/comments/create/`, { content }, authConfig())
  return res.data
}

// [추가] 보고싶어요 토글 (리뷰가 없으면 watched=False로 생성, 있으면 삭제)
// 이 기능은 로직이 복잡해서 뷰 파일 내부에서 처리하거나, 백엔드에 전용 API를 만드는 게 좋지만
// 지금은 프론트에서 create/delete를 호출하는 방식으로 구현하겠습니다.



// [추가] 보고싶어요 토글
export function toggleMovieWish(tmdbId) {
  return api.post(`/reviews/movies/${tmdbId}/wish/`)
    .then(res => res.data)
}



// [추가] 영화 리뷰 삭제
export function deleteMovieReview(reviewId) {
  return api.delete(`/reviews/${reviewId}/`, authConfig())
}

export function deleteReviewComment(commentId) {
  return api.delete(`/reviews/comments/${commentId}/`, authConfig())
}

export async function fetchMyReview(tmdbId) {
  const res = await api.get(`/reviews/movie/${tmdbId}/my/`, authConfig())
  if (res.status === 204) return null
  return res.data
}



// comet.js
export async function togglePersonLike(personId, payload) {
  // 주소 끝에 / 확인 필수
  const res = await api.post(`/movies/people/${personId}/like/`, payload, authConfig())
  return res.data
}


export async function fetchMyLikedPeople() {
  // 백엔드 URL과 일치해야 함
  const res = await api.get('/movies/me/liked-people/', authConfig())
  return res.data
}

export async function fetchFollowList(username, type) {
  const res = await api.get(`/accounts/users/${username}/follow-list/${type}/`)
  return res.data
}



// 아이디 찾기(메일로 username 안내)
export const findUsernameApi = (payload) => {
  return api.post('accounts/find-username/', payload)
}

// 비번 재설정 링크 요청(메일 전송)
export const passwordResetRequestApi = (payload) => {
  return api.post('accounts/password-reset/request/', payload)
}

// 비번 재설정 확정(uid/token + 새 비번)
export const passwordResetConfirmApi = (payload) => {
  return api.post('accounts/password-reset/confirm/', payload)
}
// 탈퇴
export const withdrawAccount = (password = '') => {

  return api.post('/accounts/withdraw/', { password })
}

